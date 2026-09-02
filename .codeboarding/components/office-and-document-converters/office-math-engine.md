---
component_id: 3.2
component_name: Office Math Engine
---

# Office Math Engine

## Component Description

A specialized utility component that performs recursive descent parsing of Office Math Markup Language (OMML). It translates XML-based math nodes into LaTeX strings to ensure mathematical formulas are accurately represented in Markdown.

---

## Key References:

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

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converter_utils/docx/pre_process.py (lines 118-156)
```
def pre_process_docx(input_docx: BinaryIO) -> BinaryIO:
    """
    Pre-processes a DOCX file with provided steps.

    The process works by unzipping the DOCX file in memory, transforming specific XML files
    (such as converting OMML elements to LaTeX), and then zipping everything back into a
    DOCX file without writing to disk.

    Args:
        input_docx (BinaryIO): A binary input stream representing the DOCX file.

    Returns:
        BinaryIO: A binary output stream representing the processed DOCX file.
    """
    output_docx = BytesIO()
    # The files that need to be pre-processed from .docx
    pre_process_enable_files = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
    ]
    with zipfile.ZipFile(input_docx, mode="r") as zip_input:
        files = {name: zip_input.read(name) for name in zip_input.namelist()}
        with zipfile.ZipFile(output_docx, mode="w") as zip_output:
            zip_output.comment = zip_input.comment
            for name, content in files.items():
                if name in pre_process_enable_files:
                    try:
                        # Pre-process the content
                        updated_content = _pre_process_math(content)
                        # In the future, if there are more pre-processing steps, they can be added here
                        zip_output.writestr(name, updated_content)
                    except Exception:
                        # If there is an error in processing the content, write the original content
                        zip_output.writestr(name, content)
                else:
                    zip_output.writestr(name, content)
    output_docx.seek(0)
    return output_docx
```


## Source Files:

- `packages/markitdown/src/markitdown/converter_utils/docx/math/omml.py`
- `packages/markitdown/src/markitdown/converter_utils/docx/pre_process.py`

