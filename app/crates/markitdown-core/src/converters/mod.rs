//! Built-in converters, one module per format. Each mirrors the behavior of
//! the corresponding `packages/markitdown/src/markitdown/converters/_*.py`.

mod audio;
mod bing_serp;
mod csv;
mod docx;
mod epub;
mod html;
mod image;
mod ipynb;
mod outlook_msg;
mod pdf;
mod plain_text;
mod pptx;
mod rss;
mod wikipedia;
mod xlsx;
mod youtube;
mod zip;

pub use audio::AudioConverter;
pub use bing_serp::BingSerpConverter;
pub use csv::CsvConverter;
pub use docx::DocxConverter;
pub use epub::EpubConverter;
pub use html::HtmlConverter;
pub use image::ImageConverter;
pub use ipynb::IpynbConverter;
pub use outlook_msg::OutlookMsgConverter;
pub use pdf::PdfConverter;
pub use plain_text::PlainTextConverter;
pub use pptx::PptxConverter;
pub use rss::RssConverter;
pub use wikipedia::WikipediaConverter;
pub use xlsx::{XlsConverter, XlsxConverter};
pub use youtube::YouTubeConverter;
pub use zip::ZipConverter;
