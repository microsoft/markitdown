import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';
import * as mammoth from 'mammoth';
import * as markdownify from 'markdownify';
import * as olefile from 'olefile';
import * as pdfminer from 'pdfminer';
import * as pptx from 'pptx';
import * as puremagic from 'puremagic';
import * as requests from 'requests';
import * as BeautifulSoup from 'beautifulsoup';
import * as charset_normalizer from 'charset-normalizer';
import * as pydub from 'pydub';
import * as sr from 'speech_recognition';
import * as YouTubeTranscriptApi from 'youtube_transcript_api';
import * as pandas from 'pandas';
import * as openai from 'openai';

class CustomMarkdownify extends markdownify.MarkdownConverter {
    constructor(options: any = {}) {
        options.heading_style = options.heading_style || markdownify.ATX;
        super(options);
    }

    convert_hn(n: number, el: any, text: string, convert_as_inline: boolean): string {
        if (!convert_as_inline) {
            if (!/^\n/.test(text)) {
                return "\n" + super.convert_hn(n, el, text, convert_as_inline);
            }
        }
        return super.convert_hn(n, el, text, convert_as_inline);
    }

    convert_a(el: any, text: string, convert_as_inline: boolean): string {
        const { prefix, suffix, text: chompedText } = markdownify.chomp(text);
        if (!chompedText) {
            return "";
        }
        let href = el.get("href");
        const title = el.get("title");

        if (href) {
            try {
                const parsed_url = new URL(href);
                if (parsed_url.protocol && !["http:", "https:", "file:"].includes(parsed_url.protocol.toLowerCase())) {
                    return `${prefix}${chompedText}${suffix}`;
                }
                href = parsed_url.toString();
            } catch (e) {
                return `${prefix}${chompedText}${suffix}`;
            }
        }

        if (this.options.autolinks && chompedText.replace(/\\_/g, "_") === href && !title && !this.options.default_title) {
            return `<${href}>`;
        }
        const title_part = title ? ` "${title.replace(/"/g, '\\"')}"` : "";
        return href ? `${prefix}[${chompedText}](${href}${title_part})${suffix}` : chompedText;
    }

    convert_img(el: any, text: string, convert_as_inline: boolean): string {
        const alt = el.attrs.alt || "";
        let src = el.attrs.src || "";
        const title = el.attrs.title || "";
        const title_part = title ? ` "${title.replace(/"/g, '\\"')}"` : "";

        if (convert_as_inline && !this.options.keep_inline_images_in.includes(el.parent.name)) {
            return alt;
        }

        if (src.startsWith("data:")) {
            src = src.split(",")[0] + "...";
        }

        return `![${alt}](${src}${title_part})`;
    }

    convert_soup(soup: any): string {
        return super.convert_soup(soup);
    }
}

class DocumentConverterResult {
    title: string | null;
    text_content: string;

    constructor(title: string | null = null, text_content: string = "") {
        this.title = title;
        this.text_content = text_content;
    }
}

abstract class DocumentConverter {
    abstract convert(local_path: string, ...args: any[]): DocumentConverterResult | null;
}

class PlainTextConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const content_type = mime.lookup(local_path) || "";
        if (!content_type.startsWith("text/") && content_type !== "application/json") {
            return null;
        }

        const text_content = fs.readFileSync(local_path, 'utf-8');
        return new DocumentConverterResult(null, text_content);
    }
}

class HtmlConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (![".html", ".htm"].includes(extension)) {
            return null;
        }

        const html_content = fs.readFileSync(local_path, 'utf-8');
        return this._convert(html_content);
    }

    _convert(html_content: string): DocumentConverterResult | null {
        const soup = new BeautifulSoup(html_content, "html.parser");

        for (const script of soup(["script", "style"])) {
            script.extract();
        }

        const body_elm = soup.find("body");
        const webpage_text = body_elm ? new CustomMarkdownify().convert_soup(body_elm) : new CustomMarkdownify().convert_soup(soup);

        return new DocumentConverterResult(soup.title ? soup.title.string : null, webpage_text);
    }
}

class RSSConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (![".xml", ".rss", ".atom"].includes(extension)) {
            return null;
        }

        const doc = new DOMParser().parseFromString(fs.readFileSync(local_path, 'utf-8'), "application/xml");
        if (doc.getElementsByTagName("rss").length > 0) {
            return this._parse_rss_type(doc);
        } else if (doc.getElementsByTagName("feed").length > 0) {
            return this._parse_atom_type(doc);
        } else {
            return null;
        }
    }

    _parse_atom_type(doc: Document): DocumentConverterResult | null {
        try {
            const root = doc.getElementsByTagName("feed")[0];
            const title = this._get_data_by_tag_name(root, "title");
            const subtitle = this._get_data_by_tag_name(root, "subtitle");
            const entries = root.getElementsByTagName("entry");
            let md_text = `# ${title}\n`;
            if (subtitle) {
                md_text += `${subtitle}\n`;
            }
            for (const entry of entries) {
                const entry_title = this._get_data_by_tag_name(entry, "title");
                const entry_summary = this._get_data_by_tag_name(entry, "summary");
                const entry_updated = this._get_data_by_tag_name(entry, "updated");
                const entry_content = this._get_data_by_tag_name(entry, "content");

                if (entry_title) {
                    md_text += `\n## ${entry_title}\n`;
                }
                if (entry_updated) {
                    md_text += `Updated on: ${entry_updated}\n`;
                }
                if (entry_summary) {
                    md_text += this._parse_content(entry_summary);
                }
                if (entry_content) {
                    md_text += this._parse_content(entry_content);
                }
            }

            return new DocumentConverterResult(title, md_text);
        } catch (e) {
            return null;
        }
    }

    _parse_rss_type(doc: Document): DocumentConverterResult | null {
        try {
            const root = doc.getElementsByTagName("rss")[0];
            const channel = root.getElementsByTagName("channel")[0];
            const channel_title = this._get_data_by_tag_name(channel, "title");
            const channel_description = this._get_data_by_tag_name(channel, "description");
            const items = channel.getElementsByTagName("item");
            let md_text = `# ${channel_title}\n`;
            if (channel_description) {
                md_text += `${channel_description}\n`;
            }
            for (const item of items) {
                const title = this._get_data_by_tag_name(item, "title");
                const description = this._get_data_by_tag_name(item, "description");
                const pubDate = this._get_data_by_tag_name(item, "pubDate");
                const content = this._get_data_by_tag_name(item, "content:encoded");

                if (title) {
                    md_text += `\n## ${title}\n`;
                }
                if (pubDate) {
                    md_text += `Published on: ${pubDate}\n`;
                }
                if (description) {
                    md_text += this._parse_content(description);
                }
                if (content) {
                    md_text += this._parse_content(content);
                }
            }

            return new DocumentConverterResult(channel_title, md_text);
        } catch (e) {
            return null;
        }
    }

    _parse_content(content: string): string {
        try {
            const soup = new BeautifulSoup(content, "html.parser");
            return new CustomMarkdownify().convert_soup(soup);
        } catch (e) {
            return content;
        }
    }

    _get_data_by_tag_name(element: Element, tag_name: string): string | null {
        const nodes = element.getElementsByTagName(tag_name);
        if (nodes.length === 0) {
            return null;
        }
        const fc = nodes[0].firstChild;
        return fc ? fc.nodeValue : null;
    }
}

class WikipediaConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        const url = args[0]?.url || "";
        if (![".html", ".htm"].includes(extension) || !/^https?:\/\/[a-zA-Z]{2,3}\.wikipedia.org\//.test(url)) {
            return null;
        }

        const html_content = fs.readFileSync(local_path, 'utf-8');
        const soup = new BeautifulSoup(html_content, "html.parser");

        for (const script of soup(["script", "style"])) {
            script.extract();
        }

        const body_elm = soup.find("div", { id: "mw-content-text" });
        const title_elm = soup.find("span", { class: "mw-page-title-main" });

        let webpage_text = "";
        let main_title = soup.title ? soup.title.string : null;

        if (body_elm) {
            if (title_elm && title_elm.length > 0) {
                main_title = title_elm.string;
            }
            webpage_text = `# ${main_title}\n\n` + new CustomMarkdownify().convert_soup(body_elm);
        } else {
            webpage_text = new CustomMarkdownify().convert_soup(soup);
        }

        return new DocumentConverterResult(main_title, webpage_text);
    }
}

class YouTubeConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        const url = args[0]?.url || "";
        if (![".html", ".htm"].includes(extension) || !url.startsWith("https://www.youtube.com/watch?")) {
            return null;
        }

        const html_content = fs.readFileSync(local_path, 'utf-8');
        const soup = new BeautifulSoup(html_content, "html.parser");

        const metadata: { [key: string]: string } = { title: soup.title ? soup.title.string : "" };
        for (const meta of soup(["meta"])) {
            for (const a in meta.attrs) {
                if (["itemprop", "property", "name"].includes(a)) {
                    metadata[meta[a]] = meta.get("content", "");
                    break;
                }
            }
        }

        try {
            for (const script of soup(["script"])) {
                const content = script.text;
                if (content.includes("ytInitialData")) {
                    const lines = content.split(/\r?\n/);
                    const obj_start = lines[0].indexOf("{");
                    const obj_end = lines[0].lastIndexOf("}");
                    if (obj_start >= 0 && obj_end >= 0) {
                        const data = JSON.parse(lines[0].substring(obj_start, obj_end + 1));
                        const attrdesc = this._findKey(data, "attributedDescriptionBodyText");
                        if (attrdesc) {
                            metadata["description"] = attrdesc.content;
                        }
                    }
                    break;
                }
            }
        } catch (e) {}

        let webpage_text = "# YouTube\n";
        const title = this._get(metadata, ["title", "og:title", "name"]) || "";
        if (title) {
            webpage_text += `\n## ${title}\n`;
        }

        let stats = "";
        const views = this._get(metadata, ["interactionCount"]);
        if (views) {
            stats += `- **Views:** ${views}\n`;
        }

        const keywords = this._get(metadata, ["keywords"]);
        if (keywords) {
            stats += `- **Keywords:** ${keywords}\n`;
        }

        const runtime = this._get(metadata, ["duration"]);
        if (runtime) {
            stats += `- **Runtime:** ${runtime}\n`;
        }

        if (stats) {
            webpage_text += `\n### Video Metadata\n${stats}\n`;
        }

        const description = this._get(metadata, ["description", "og:description"]);
        if (description) {
            webpage_text += `\n### Description\n${description}\n`;
        }

        if (YouTubeTranscriptApi) {
            let transcript_text = "";
            const parsed_url = new URL(url);
            const params = new URLSearchParams(parsed_url.search);
            if (params.has("v")) {
                const video_id = params.get("v");
                try {
                    const youtube_transcript_languages = args[0]?.youtube_transcript_languages || ["en"];
                    const transcript = YouTubeTranscriptApi.getTranscript(video_id, { languages: youtube_transcript_languages });
                    transcript_text = transcript.map((part: any) => part.text).join(" ");
                } catch (e) {}
            }
            if (transcript_text) {
                webpage_text += `\n### Transcript\n${transcript_text}\n`;
            }
        }

        return new DocumentConverterResult(title, webpage_text);
    }

    _get(metadata: { [key: string]: string }, keys: string[], defaultValue: string | null = null): string | null {
        for (const key of keys) {
            if (metadata[key]) {
                return metadata[key];
            }
        }
        return defaultValue;
    }

    _findKey(json: any, key: string): any {
        if (Array.isArray(json)) {
            for (const elm of json) {
                const ret = this._findKey(elm, key);
                if (ret !== null) {
                    return ret;
                }
            }
        } else if (typeof json === "object") {
            for (const k in json) {
                if (k === key) {
                    return json[k];
                } else {
                    const ret = this._findKey(json[k], key);
                    if (ret !== null) {
                        return ret;
                    }
                }
            }
        }
        return null;
    }
}

class IpynbConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".ipynb") {
            return null;
        }

        const notebook_content = JSON.parse(fs.readFileSync(local_path, 'utf-8'));
        return this._convert(notebook_content);
    }

    _convert(notebook_content: any): DocumentConverterResult | null {
        try {
            const md_output: string[] = [];
            let title: string | null = null;

            for (const cell of notebook_content.cells) {
                const cell_type = cell.cell_type;
                const source_lines = cell.source;

                if (cell_type === "markdown") {
                    md_output.push(source_lines.join(""));

                    if (!title) {
                        for (const line of source_lines) {
                            if (line.startsWith("# ")) {
                                title = line.replace(/^# /, "").trim();
                                break;
                            }
                        }
                    }
                } else if (cell_type === "code") {
                    md_output.push(`\`\`\`python\n${source_lines.join("")}\n\`\`\``);
                } else if (cell_type === "raw") {
                    md_output.push(`\`\`\`\n${source_lines.join("")}\n\`\`\``);
                }
            }

            const md_text = md_output.join("\n\n");
            title = notebook_content.metadata.title || title;

            return new DocumentConverterResult(title, md_text);
        } catch (e) {
            throw new Error(`Error converting .ipynb file: ${e.message}`);
        }
    }
}

class BingSerpConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        const url = args[0]?.url || "";
        if (![".html", ".htm"].includes(extension) || !/^https:\/\/www\.bing\.com\/search\?q=/.test(url)) {
            return null;
        }

        const html_content = fs.readFileSync(local_path, 'utf-8');
        const soup = new BeautifulSoup(html_content, "html.parser");

        for (const tptt of soup.find_all({ class: "tptt" })) {
            if (tptt.string) {
                tptt.string += " ";
            }
        }
        for (const slug of soup.find_all({ class: "algoSlug_icon" })) {
            slug.extract();
        }

        const results: string[] = [];
        for (const result of soup.find_all({ class: "b_algo" })) {
            for (const a of result.find_all("a", { href: true })) {
                const parsed_href = new URL(a.attrs.href);
                const qs = new URLSearchParams(parsed_href.search);

                if (qs.has("u")) {
                    let u = qs.get("u") || "";
                    u = u.slice(2).trim() + "==";

                    try {
                        a.attrs.href = Buffer.from(u, "base64").toString("utf-8");
                    } catch (e) {}
                }
            }

            const md_result = new CustomMarkdownify().convert_soup(result).trim();
            const lines = md_result.split(/\n+/).map(line => line.trim());
            results.push(lines.filter(line => line.length > 0).join("\n"));
        }

        const query = new URLSearchParams(new URL(url).search).get("q") || "";
        const webpage_text = `## A Bing search for '${query}' found the following results:\n\n${results.join("\n\n")}`;

        return new DocumentConverterResult(soup.title ? soup.title.string : null, webpage_text);
    }
}

class PdfConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".pdf") {
            return null;
        }

        const text_content = pdfminer.high_level.extract_text(local_path);
        return new DocumentConverterResult(null, text_content);
    }
}

class DocxConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".docx") {
            return null;
        }

        const result = mammoth.convert_to_html({ path: local_path });
        return this._convert(result.value);
    }
}

class XlsxConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".xlsx") {
            return null;
        }

        const sheets = pandas.read_excel(local_path, { sheet_name: null, engine: "openpyxl" });
        let md_content = "";
        for (const sheet in sheets) {
            md_content += `## ${sheet}\n`;
            const html_content = sheets[sheet].to_html({ index: false });
            md_content += this._convert(html_content).text_content.trim() + "\n\n";
        }

        return new DocumentConverterResult(null, md_content.trim());
    }
}

class XlsConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".xls") {
            return null;
        }

        const sheets = pandas.read_excel(local_path, { sheet_name: null, engine: "xlrd" });
        let md_content = "";
        for (const sheet in sheets) {
            md_content += `## ${sheet}\n`;
            const html_content = sheets[sheet].to_html({ index: false });
            md_content += this._convert(html_content).text_content.trim() + "\n\n";
        }

        return new DocumentConverterResult(null, md_content.trim());
    }
}

class PptxConverter extends HtmlConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".pptx") {
            return null;
        }

        const presentation = new pptx.Presentation(local_path);
        let md_content = "";
        let slide_num = 0;
        for (const slide of presentation.slides) {
            slide_num += 1;
            md_content += `\n\n<!-- Slide number: ${slide_num} -->\n`;

            const title = slide.shapes.title;
            for (const shape of slide.shapes) {
                if (this._is_picture(shape)) {
                    let alt_text = "";
                    try {
                        alt_text = shape._element._nvXxPr.cNvPr.attrib.descr || "";
                    } catch (e) {}

                    const filename = shape.name.replace(/\W/g, "") + ".jpg";
                    md_content += `\n![${alt_text || shape.name}](${filename})\n`;
                }

                if (this._is_table(shape)) {
                    let html_table = "<html><body><table>";
                    let first_row = true;
                    for (const row of shape.table.rows) {
                        html_table += "<tr>";
                        for (const cell of row.cells) {
                            if (first_row) {
                                html_table += `<th>${html.escape(cell.text)}</th>`;
                            } else {
                                html_table += `<td>${html.escape(cell.text)}</td>`;
                            }
                        }
                        html_table += "</tr>";
                        first_row = false;
                    }
                    html_table += "</table></body></html>";
                    md_content += `\n${this._convert(html_table).text_content.trim()}\n`;
                }

                if (shape.has_chart) {
                    md_content += this._convert_chart_to_markdown(shape.chart);
                } else if (shape.has_text_frame) {
                    if (shape === title) {
                        md_content += `# ${shape.text.trim()}\n`;
                    } else {
                        md_content += `${shape.text.trim()}\n`;
                    }
                }
            }

            if (slide.has_notes_slide) {
                md_content += "\n\n### Notes:\n";
                const notes_frame = slide.notes_slide.notes_text_frame;
                if (notes_frame) {
                    md_content += notes_frame.text.trim();
                }
            }
        }

        return new DocumentConverterResult(null, md_content.trim());
    }

    _is_picture(shape: any): boolean {
        return shape.shape_type === pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE || (shape.shape_type === pptx.enum.shapes.MSO_SHAPE_TYPE.PLACEHOLDER && shape.image);
    }

    _is_table(shape: any): boolean {
        return shape.shape_type === pptx.enum.shapes.MSO_SHAPE_TYPE.TABLE;
    }

    _convert_chart_to_markdown(chart: any): string {
        let md = "\n\n### Chart";
        if (chart.has_title) {
            md += `: ${chart.chart_title.text_frame.text}`;
        }
        md += "\n\n";
        const data: any[] = [];
        const category_names = chart.plots[0].categories.map((c: any) => c.label);
        const series_names = chart.series.map((s: any) => s.name);
        data.push(["Category", ...series_names]);

        for (let i = 0; i < category_names.length; i++) {
            const row = [category_names[i]];
            for (const series of chart.series) {
                row.push(series.values[i]);
            }
            data.push(row);
        }

        const markdown_table = data.map(row => `| ${row.join(" | ")} |`);
        const header = markdown_table[0];
        const separator = `|${"|".repeat(data[0].length - 1)}|`;
        return md + [header, separator, ...markdown_table.slice(1)].join("\n");
    }
}

class MediaConverter extends DocumentConverter {
    _get_metadata(local_path: string, exiftool_path?: string): any {
        if (!exiftool_path) {
            const which_exiftool = which("exiftool");
            if (which_exiftool) {
                console.warn(`Implicit discovery of 'exiftool' is disabled. If you would like to continue to use exiftool in MarkItDown, please set the exiftool_path parameter in the MarkItDown constructor. E.g., md = new MarkItDown({ exiftool_path: "${which_exiftool}" })`);
            }
            return null;
        } else {
            try {
                const result = execSync(`${exiftool_path} -json ${local_path}`).toString();
                return JSON.parse(result)[0];
            } catch (e) {
                return null;
            }
        }
    }
}

class WavConverter extends MediaConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".wav") {
            return null;
        }

        let md_content = "";

        const metadata = this._get_metadata(local_path, args[0]?.exiftool_path);
        if (metadata) {
            for (const f of ["Title", "Artist", "Author", "Band", "Album", "Genre", "Track", "DateTimeOriginal", "CreateDate", "Duration"]) {
                if (metadata[f]) {
                    md_content += `${f}: ${metadata[f]}\n`;
                }
            }
        }

        if (sr) {
            try {
                const transcript = this._transcribe_audio(local_path);
                md_content += `\n\n### Audio Transcript:\n${transcript || "[No speech detected]"}`;
            } catch (e) {
                md_content += "\n\n### Audio Transcript:\nError. Could not transcribe this audio.";
            }
        }

        return new DocumentConverterResult(null, md_content.trim());
    }

    _transcribe_audio(local_path: string): string {
        const recognizer = new sr.Recognizer();
        const audio = recognizer.record(new sr.AudioFile(local_path));
        return recognizer.recognize_google(audio).trim();
    }
}

class Mp3Converter extends WavConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".mp3") {
            return null;
        }

        let md_content = "";

        const metadata = this._get_metadata(local_path, args[0]?.exiftool_path);
        if (metadata) {
            for (const f of ["Title", "Artist", "Author", "Band", "Album", "Genre", "Track", "DateTimeOriginal", "CreateDate", "Duration"]) {
                if (metadata[f]) {
                    md_content += `${f}: ${metadata[f]}\n`;
                }
            }
        }

        if (sr && pydub) {
            const temp_path = path.join(os.tmpdir(), `${path.basename(local_path, ".mp3")}.wav`);
            try {
                const sound = pydub.AudioSegment.from_mp3(local_path);
                sound.export(temp_path, { format: "wav" });

                const transcript = this._transcribe_audio(temp_path).trim();
                md_content += `\n\n### Audio Transcript:\n${transcript || "[No speech detected]"}`;
            } catch (e) {
                md_content += "\n\n### Audio Transcript:\nError. Could not transcribe this audio.";
            } finally {
                fs.unlinkSync(temp_path);
            }
        }

        return new DocumentConverterResult(null, md_content.trim());
    }
}

class ImageConverter extends MediaConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (![".jpg", ".jpeg", ".png"].includes(extension)) {
            return null;
        }

        let md_content = "";

        const metadata = this._get_metadata(local_path, args[0]?.exiftool_path);
        if (metadata) {
            for (const f of ["ImageSize", "Title", "Caption", "Description", "Keywords", "Artist", "Author", "DateTimeOriginal", "CreateDate", "GPSPosition"]) {
                if (metadata[f]) {
                    md_content += `${f}: ${metadata[f]}\n`;
                }
            }
        }

        const llm_client = args[0]?.llm_client;
        const llm_model = args[0]?.llm_model;
        if (llm_client && llm_model) {
            md_content += `\n# Description:\n${this._get_llm_description(local_path, extension, llm_client, llm_model, args[0]?.llm_prompt).trim()}\n`;
        }

        return new DocumentConverterResult(null, md_content);
    }

    _get_llm_description(local_path: string, extension: string, client: any, model: string, prompt: string = "Write a detailed caption for this image."): string {
        const content_type = mime.lookup(extension) || "image/jpeg";
        const image_base64 = fs.readFileSync(local_path, 'base64');
        const data_uri = `data:${content_type};base64,${image_base64}`;

        const messages = [
            {
                role: "user",
                content: [
                    { type: "text", text: prompt },
                    { type: "image_url", image_url: { url: data_uri } }
                ]
            }
        ];

        const response = client.chat.completions.create({ model, messages });
        return response.choices[0].message.content;
    }
}

class OutlookMsgConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".msg") {
            return null;
        }

        try {
            const msg = new olefile.OleFileIO(local_path);
            let md_content = "# Email Message\n\n";

            const headers = {
                "From": this._get_stream_data(msg, "__substg1.0_0C1F001F"),
                "To": this._get_stream_data(msg, "__substg1.0_0E04001F"),
                "Subject": this._get_stream_data(msg, "__substg1.0_0037001F")
            };

            for (const key in headers) {
                if (headers[key]) {
                    md_content += `**${key}:** ${headers[key]}\n`;
                }
            }

            md_content += "\n## Content\n\n";
            const body = this._get_stream_data(msg, "__substg1.0_1000001F");
            if (body) {
                md_content += body;
            }

            msg.close();
            return new DocumentConverterResult(headers.Subject, md_content.trim());
        } catch (e) {
            throw new Error(`Could not convert MSG file '${local_path}': ${e.message}`);
        }
    }

    _get_stream_data(msg: any, stream_path: string): string | null {
        try {
            if (msg.exists(stream_path)) {
                const data = msg.openstream(stream_path).read();
                try {
                    return data.toString("utf-16le").trim();
                } catch (e) {
                    try {
                        return data.toString("utf-8").trim();
                    } catch (e) {
                        return data.toString("utf-8", { errors: "ignore" }).trim();
                    }
                }
            }
        } catch (e) {}
        return null;
    }
}

class ZipConverter extends DocumentConverter {
    convert(local_path: string, ...args: any[]): DocumentConverterResult | null {
        const extension = path.extname(local_path).toLowerCase();
        if (extension !== ".zip") {
            return null;
        }

        const parent_converters = args[0]?._parent_converters || [];
        if (!parent_converters.length) {
            return new DocumentConverterResult(null, `[ERROR] No converters available to process zip contents from: ${local_path}`);
        }

        const extracted_zip_folder_name = `extracted_${path.basename(local_path, ".zip")}_zip`;
        const extraction_dir = path.join(path.dirname(local_path), extracted_zip_folder_name);
        let md_content = `Content from the zip file \`${path.basename(local_path)}\`:\n\n`;

        try {
            const zip = new AdmZip(local_path);
            zip.extractAllTo(extraction_dir, true);

            for (const file of zip.getEntries()) {
                const file_path = path.join(extraction_dir, file.entryName);
                const relative_path = path.relative(extraction_dir, file_path);
                const file_extension = path.extname(file_path);

                const file_args = { ...args[0], file_extension, _parent_converters: parent_converters };
                for (const converter of parent_converters) {
                    if (converter instanceof ZipConverter) {
                        continue;
                    }

                    const result = converter.convert(file_path, file_args);
                    if (result) {
                        md_content += `\n## File: ${relative_path}\n\n${result.text_content}\n\n`;
                        break;
                    }
                }
            }

            if (args[0]?.cleanup_extracted !== false) {
                fs.rmdirSync(extraction_dir, { recursive: true });
            }

            return new DocumentConverterResult(null, md_content.trim());
        } catch (e) {
            return new DocumentConverterResult(null, `[ERROR] Failed to process zip file ${local_path}: ${e.message}`);
        }
    }
}

class MarkItDown {
    private _requests_session: any;
    private _llm_client: any;
    private _llm_model: string | null;
    private _style_map: string | null;
    private _exiftool_path: string | null;
    private _page_converters: DocumentConverter[];

    constructor(options: any = {}) {
        this._requests_session = options.requests_session || new requests.Session();
        this._llm_client = options.llm_client || null;
        this._llm_model = options.llm_model || null;
        this._style_map = options.style_map || null;
        this._exiftool_path = options.exiftool_path || process.env.EXIFTOOL_PATH || null;

        this._page_converters = [];

        this.register_page_converter(new PlainTextConverter());
        this.register_page_converter(new HtmlConverter());
        this.register_page_converter(new RSSConverter());
        this.register_page_converter(new WikipediaConverter());
        this.register_page_converter(new YouTubeConverter());
        this.register_page_converter(new BingSerpConverter());
        this.register_page_converter(new DocxConverter());
        this.register_page_converter(new XlsxConverter());
        this.register_page_converter(new XlsConverter());
        this.register_page_converter(new PptxConverter());
        this.register_page_converter(new WavConverter());
        this.register_page_converter(new Mp3Converter());
        this.register_page_converter(new ImageConverter());
        this.register_page_converter(new IpynbConverter());
        this.register_page_converter(new PdfConverter());
        this.register_page_converter(new ZipConverter());
        this.register_page_converter(new OutlookMsgConverter());
    }

    convert(source: string | requests.Response | Path, ...args: any[]): DocumentConverterResult {
        if (typeof source === "string") {
            if (/^https?:\/\//.test(source) || /^file:\/\//.test(source)) {
                return this.convert_url(source, ...args);
            } else {
                return this.convert_local(source, ...args);
            }
        } else if (source instanceof requests.Response) {
            return this.convert_response(source, ...args);
        } else if (source instanceof Path) {
            return this.convert_local(source.toString(), ...args);
        }
    }

    convert_local(path: string, ...args: any[]): DocumentConverterResult {
        const extensions = [args[0]?.file_extension || null];
        const ext = path.extname(path);
        if (ext) {
            extensions.push(ext);
        }

        for (const g of this._guess_ext_magic(path)) {
            extensions.push(g);
        }

        return this._convert(path, extensions, ...args);
    }

    convert_stream(stream: any, ...args: any[]): DocumentConverterResult {
        const extensions = [args[0]?.file_extension || null];
        const temp_path = path.join(os.tmpdir(), `temp_${Date.now()}`);
        fs.writeFileSync(temp_path, stream);

        for (const g of this._guess_ext_magic(temp_path)) {
            extensions.push(g);
        }

        const result = this._convert(temp_path, extensions, ...args);
        fs.unlinkSync(temp_path);
        return result;
    }

    convert_url(url: string, ...args: any[]): DocumentConverterResult {
        const response = this._requests_session.get(url, { responseType: 'stream' });
        return this.convert_response(response, ...args);
    }

    convert_response(response: any, ...args: any[]): DocumentConverterResult {
        const extensions = [args[0]?.file_extension || null];
        const content_type = response.headers['content-type'].split(";")[0];
        const ext = mime.extension(content_type);
        if (ext) {
            extensions.push(ext);
        }

        const content_disposition = response.headers['content-disposition'] || "";
        const filename_match = content_disposition.match(/filename=([^;]+)/);
        if (filename_match) {
            const filename_ext = path.extname(filename_match[1].replace(/['"]/g, ""));
            if (filename_ext) {
                extensions.push(filename_ext);
            }
        }

        const url_ext = path.extname(new URL(response.url).pathname);
        if (url_ext) {
            extensions.push(url_ext);
        }

        const temp_path = path.join(os.tmpdir(), `temp_${Date.now()}`);
        const writer = fs.createWriteStream(temp_path);
        response.data.pipe(writer);

        return new Promise((resolve, reject) => {
            writer.on('finish', () => {
                for (const g of this._guess_ext_magic(temp_path)) {
                    extensions.push(g);
                }

                const result = this._convert(temp_path, extensions, ...args);
                fs.unlinkSync(temp_path);
                resolve(result);
            });
            writer.on('error', reject);
        });
    }

    _convert(local_path: string, extensions: (string | null)[], ...args: any[]): DocumentConverterResult {
        for (const ext of extensions) {
            for (const converter of this._page_converters) {
                const file_args = { ...args[0], file_extension: ext };
                try {
                    const result = converter.convert(local_path, file_args);
                    if (result) {
                        result.text_content = result.text_content.split(/\r?\n/).map(line => line.trimEnd()).join("\n");
                        result.text_content = result.text_content.replace(/\n{3,}/g, "\n\n");
                        return result;
                    }
                } catch (e) {
                    console.error(e);
                }
            }
        }

        throw new Error(`Could not convert '${local_path}' to Markdown. The formats ${extensions} are not supported.`);
    }

    _guess_ext_magic(path: string): string[] {
        try {
            const guesses = puremagic.magic_file(path);
            if (!guesses.length) {
                const file = fs.createReadStream(path);
                const trimmed_file = file.pipe(new stream.Transform({
                    transform(chunk, encoding, callback) {
                        this.push(chunk.toString().trimStart());
                        callback();
                    }
                }));
                guesses.push(...puremagic.magic_stream(trimmed_file));
            }

            return guesses.map(g => g.extension.startsWith(".") ? g.extension : `.${g.extension}`);
        } catch (e) {
            return [];
        }
    }

    register_page_converter(converter: DocumentConverter): void {
        this._page_converters.unshift(converter);
    }
}
