# -*- coding: utf-8 -*-

"""
Office Math Markup Language (OMML)
Adapted from https://github.com/xiilei/dwml/blob/master/dwml/omml.py
On 25/03/2025
"""

from defusedxml import ElementTree as ET

from .latex_dict import (
    CHARS,
    CHR,
    CHR_BO,
    CHR_DEFAULT,
    POS,
    POS_DEFAULT,
    SUB,
    SUP,
    F,
    F_DEFAULT,
    T,
    FUNC,
    D,
    D_DEFAULT,
    RAD,
    RAD_DEFAULT,
    ARR,
    LIM_FUNC,
    LIM_TO,
    LIM_UPP,
    M,
    BRK,
    BLANK,
    BACKSLASH,
    ALN,
    FUNC_PLACE,
)

OMML_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def load(stream):
    tree = ET.parse(stream)
    for omath in tree.findall(OMML_NS + "oMath"):
        yield oMath2Latex(omath)


def load_string(string):
    root = ET.fromstring(string)
    for omath in root.findall(OMML_NS + "oMath"):
        yield oMath2Latex(omath)


def escape_latex(strs):
    last = None
    new_chr = []
    strs = strs.replace(r"\\", "\\")
    for c in strs:
        if (c in CHARS) and (last != BACKSLASH):
            new_chr.append(BACKSLASH + c)
        else:
            new_chr.append(c)
        last = c
    return BLANK.join(new_chr)


def get_val(key, default=None, store=CHR):
    if key is not None:
        return key if not store else store.get(key, key)
    else:
        return default


class Tag2Method(object):
    def call_method(self, elm, stag=None):
        getmethod = self.tag2meth.get
        if stag is None:
            stag = elm.tag.replace(OMML_NS, "")
        method = getmethod(stag)
        if method:
            return method(self, elm)
        else:
            return None

    def process_children_list(self, elm, include=None):
        """
        process children of the elm,return iterable
        """
        for _e in list(elm):
            if OMML_NS not in _e.tag:
                continue
            stag = _e.tag.replace(OMML_NS, "")
            if include and (stag not in include):
                continue
            t = self.call_method(_e, stag=stag)
            if t is None:
                t = self.process_unknow(_e, stag)
                if t is None:
                    continue
            yield (stag, t, _e)

    def process_children_dict(self, elm, include=None):
        """
        process children of the elm,return dict
        """
        latex_chars = dict()
        for stag, t, e in self.process_children_list(elm, include):
            latex_chars[stag] = t
        return latex_chars

    def process_children(self, elm, include=None):
        """
        process children of the elm,return string
        """
        return BLANK.join(
            (
                t if not isinstance(t, Tag2Method) else str(t)
                for stag, t, e in self.process_children_list(elm, include)
            )
        )

    def process_unknow(self, elm, stag):
        return None


class Pr(Tag2Method):
    text = ""

    __val_tags = ("chr", "pos", "begChr", "endChr", "type")

    __innerdict = None  # can't use the __dict__

    """ common properties of element"""

    def __init__(self, elm):
        self.__innerdict = {}
        self.text = self.process_children(elm)

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.__str__(self)

    def __getattr__(self, name):
        return self.__innerdict.get(name, None)

    def do_brk(self, elm):
        self.__innerdict["brk"] = BRK
        return BRK

    def do_common(self, elm):
        stag = elm.tag.replace(OMML_NS, "")
        if stag in self.__val_tags:
            t = elm.get("{0}val".format(OMML_NS))
            self.__innerdict[stag] = t
        return None

    tag2meth = {
        "brk": do_brk,
        "chr": do_common,
        "pos": do_common,
        "begChr": do_common,
        "endChr": do_common,
        "type": do_common,
    }


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
