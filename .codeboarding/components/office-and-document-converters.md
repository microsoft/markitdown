---
component_id: 3
component_name: Office & Document Converters
---

# Office & Document Converters

## Component Description

Manages complex binary formats including PDF, DOCX, and PPTX. It includes a specialized recursive descent parser for converting Office Math (OMML) to LaTeX to preserve mathematical expressions.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_docx_converter.py (lines 31-83)
```
class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".docx",
                    feature="docx",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        style_map = kwargs.get("style_map", None)
        pre_process_stream = pre_process_docx(file_stream)
        return self._html_converter.convert_string(
            mammoth.convert_to_html(pre_process_stream, style_map=style_map).value,
            **kwargs,
        )
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_pdf_converter.py (lines 495-589)
```
class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown.
    Supports extracting tables into aligned Markdown format (via pdfplumber).
    Falls back to pdfminer if pdfplumber is missing or fails.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        assert isinstance(file_stream, io.IOBase)

        # Read file stream into BytesIO for compatibility with pdfplumber
        pdf_bytes = io.BytesIO(file_stream.read())

        try:
            # Single pass: check every page for form-style content.
            # Pages with tables/forms get rich extraction; plain-text
            # pages are collected separately. page.close() is called
            # after each page to free pdfplumber's cached objects and
            # keep memory usage constant regardless of page count.
            markdown_chunks: list[str] = []
            form_page_count = 0
            plain_page_indices: list[int] = []

            with pdfplumber.open(pdf_bytes) as pdf:
                for page_idx, page in enumerate(pdf.pages):
                    page_content = _extract_form_content_from_words(page)

                    if page_content is not None:
                        form_page_count += 1
                        if page_content.strip():
                            markdown_chunks.append(page_content)
                    else:
                        plain_page_indices.append(page_idx)
                        text = page.extract_text()
                        if text and text.strip():
                            markdown_chunks.append(text.strip())

                    page.close()  # Free cached page data immediately

            # If no pages had form-style content, use pdfminer for
            # the whole document (better text spacing for prose).
            if form_page_count == 0:
                pdf_bytes.seek(0)
                markdown = pdfminer.high_level.extract_text(pdf_bytes)
            else:
                markdown = "\n\n".join(markdown_chunks).strip()

        except Exception:
            # Fallback if pdfplumber fails
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Fallback if still empty
        if not markdown:
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Post-process to merge MasterFormat-style partial numbering with following text
        markdown = _merge_partial_numbering_lines(markdown)

        return DocumentConverterResult(markdown=markdown)
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converter_utils/docx/math/omml.py (lines 170-400)
```
class oMath2Latex(Tag2Method):
    """
    Convert oMath element of omml to latex
    """

    _t_dict = T

    __direct_tags = ("box", "sSub", "sSup", "sSubSup", "num", "den", "deg", "e")

    def __init__(self, element):
        self._latex = self.process_children(element)

    def __str__(self):
        return self.latex

    def __unicode__(self):
        return self.__str__(self)

    def process_unknow(self, elm, stag):
        if stag in self.__direct_tags:
            return self.process_children(elm)
        elif stag[-2:] == "Pr":
            return Pr(elm)
        else:
            return None

    @property
    def latex(self):
        return self._latex

    def do_acc(self, elm):
        """
        the accent function
        """
        c_dict = self.process_children_dict(elm)
        latex_s = get_val(
            c_dict["accPr"].chr, default=CHR_DEFAULT.get("ACC_VAL"), store=CHR
        )
        return latex_s.format(c_dict["e"])

    def do_bar(self, elm):
        """
        the bar function
        """
        c_dict = self.process_children_dict(elm)
        pr = c_dict["barPr"]
        latex_s = get_val(pr.pos, default=POS_DEFAULT.get("BAR_VAL"), store=POS)
        return pr.text + latex_s.format(c_dict["e"])

    def do_d(self, elm):
        """
        the delimiter object
        """
        c_dict = self.process_children_dict(elm)
        pr = c_dict["dPr"]
        null = D_DEFAULT.get("null")
        s_val = get_val(pr.begChr, default=D_DEFAULT.get("left"), store=T)
        e_val = get_val(pr.endChr, default=D_DEFAULT.get("right"), store=T)
        return pr.text + D.format(
            left=null if not s_val else escape_latex(s_val),
            text=c_dict["e"],
            right=null if not e_val else escape_latex(e_val),
        )

    def do_spre(self, elm):
        """
        the Pre-Sub-Superscript object -- Not support yet
        """
        pass

    def do_sub(self, elm):
        text = self.process_children(elm)
        return SUB.format(text)

    def do_sup(self, elm):
        text = self.process_children(elm)
        return SUP.format(text)

    def do_f(self, elm):
        """
        the fraction object
        """
        c_dict = self.process_children_dict(elm)
        pr = c_dict["fPr"]
        latex_s = get_val(pr.type, default=F_DEFAULT, store=F)
        return pr.text + latex_s.format(num=c_dict.get("num"), den=c_dict.get("den"))

    def do_func(self, elm):
        """
        the Function-Apply object (Examples:sin cos)
        """
        c_dict = self.process_children_dict(elm)
        func_name = c_dict.get("fName")
        return func_name.replace(FUNC_PLACE, c_dict.get("e"))

    def do_fname(self, elm):
        """
        the func name
        """
        latex_chars = []
        for stag, t, e in self.process_children_list(elm):
            if stag == "r":
                if FUNC.get(t):
                    latex_chars.append(FUNC[t])
                else:
                    raise NotImplementedError("Not support func %s" % t)
            else:
                latex_chars.append(t)
        t = BLANK.join(latex_chars)
        return t if FUNC_PLACE in t else t + FUNC_PLACE  # do_func will replace this

    def do_groupchr(self, elm):
        """
        the Group-Character object
        """
        c_dict = self.process_children_dict(elm)
        pr = c_dict["groupChrPr"]
        latex_s = get_val(pr.chr)
        return pr.text + latex_s.format(c_dict["e"])

    def do_rad(self, elm):
        """
        the radical object
        """
        c_dict = self.process_children_dict(elm)
        text = c_dict.get("e")
        deg_text = c_dict.get("deg")
        if deg_text:
            return RAD.format(deg=deg_text, text=text)
        else:
            return RAD_DEFAULT.format(text=text)

    def do_eqarr(self, elm):
        """
        the Array object
        """
        return ARR.format(
            text=BRK.join(
                [t for stag, t, e in self.process_children_list(elm, include=("e",))]
            )
        )

    def do_limlow(self, elm):
        """
        the Lower-Limit object
        """
        t_dict = self.process_children_dict(elm, include=("e", "lim"))
        latex_s = LIM_FUNC.get(t_dict["e"])
        if not latex_s:
            raise NotImplementedError("Not support lim %s" % t_dict["e"])
        else:
            return latex_s.format(lim=t_dict.get("lim"))

    def do_limupp(self, elm):
        """
        the Upper-Limit object
        """
        t_dict = self.process_children_dict(elm, include=("e", "lim"))
        return LIM_UPP.format(lim=t_dict.get("lim"), text=t_dict.get("e"))

    def do_lim(self, elm):
        """
        the lower limit of the limLow object and the upper limit of the limUpp function
        """
        return self.process_children(elm).replace(LIM_TO[0], LIM_TO[1])

    def do_m(self, elm):
        """
        the Matrix object
        """
        rows = []
        for stag, t, e in self.process_children_list(elm):
            if stag == "mPr":
                pass
            elif stag == "mr":
                rows.append(t)
        return M.format(text=BRK.join(rows))

    def do_mr(self, elm):
        """
        a single row of the matrix m
        """
        return ALN.join(
            [t for stag, t, e in self.process_children_list(elm, include=("e",))]
        )

    def do_nary(self, elm):
        """
        the n-ary object
        """
        res = []
        bo = ""
        for stag, t, e in self.process_children_list(elm):
            if stag == "naryPr":
                bo = get_val(t.chr, store=CHR_BO)
            else:
                res.append(t)
        return bo + BLANK.join(res)

    def do_r(self, elm):
        """
        Get text from 'r' element,And try convert them to latex symbols
        @todo text style support , (sty)
        @todo \text (latex pure text support)
        """
        _str = []
        for s in elm.findtext("./{0}t".format(OMML_NS)):
            # s = s if isinstance(s,unicode) else unicode(s,'utf-8')
            _str.append(self._t_dict.get(s, s))
        return escape_latex(BLANK.join(_str))

    tag2meth = {
        "acc": do_acc,
        "r": do_r,
        "bar": do_bar,
        "sub": do_sub,
        "sup": do_sup,
        "f": do_f,
        "func": do_func,
        "fName": do_fname,
        "groupChr": do_groupchr,
        "d": do_d,
        "rad": do_rad,
        "eqArr": do_eqarr,
        "limLow": do_limlow,
        "limUpp": do_limupp,
        "lim": do_lim,
        "m": do_m,
        "mr": do_mr,
        "nary": do_nary,
    }
```


## Source Files:

- `packages/markitdown/src/markitdown/_exceptions.py`
- `packages/markitdown/src/markitdown/converter_utils/docx/math/omml.py`
- `packages/markitdown/src/markitdown/converter_utils/docx/pre_process.py`
- `packages/markitdown/src/markitdown/converters/_doc_intel_converter.py`
- `packages/markitdown/src/markitdown/converters/_docx_converter.py`
- `packages/markitdown/src/markitdown/converters/_html_converter.py`
- `packages/markitdown/src/markitdown/converters/_llm_caption.py`
- `packages/markitdown/src/markitdown/converters/_outlook_msg_converter.py`
- `packages/markitdown/src/markitdown/converters/_pdf_converter.py`
- `packages/markitdown/src/markitdown/converters/_pptx_converter.py`
- `packages/markitdown/src/markitdown/converters/_xlsx_converter.py`

