from markitdown.converter_utils.docx.math.omml import load_string


def test_omml_known_function():
    omml_xml = """<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
        <m:oMath>
            <m:func>
                <m:fName><m:r><m:t>log</m:t></m:r></m:fName>
                <m:e><m:r><m:t>x</m:t></m:r></m:e>
            </m:func>
        </m:oMath>
    </m:oMathPara>"""
    results = list(load_string(omml_xml))
    assert len(results) == 1
    assert r"\log" in str(results[0])


def test_omml_unknown_function_fallback():
    omml_xml = """<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
        <m:oMath>
            <m:func>
                <m:fName><m:r><m:t>customFunc</m:t></m:r></m:fName>
                <m:e><m:r><m:t>x</m:t></m:r></m:e>
            </m:func>
        </m:oMath>
    </m:oMathPara>"""
    results = list(load_string(omml_xml))
    assert len(results) == 1
    assert r"\operatorname{customFunc}" in str(results[0])
