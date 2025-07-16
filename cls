[33mda7bcea[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m, [m[1;31morigin/HEAD[m[33m)[m docs: rephrase sentence (#1278)
[33m3bfb821[m Have the MarkItDown MCP server read MARKITDOWN_ENABLE_PLUGINS from ENV (#1273)
[33m62b7228[m pin onnxruntime on Windows (#1274)
[33m1dd3c83[m Promoting 0.1.2a1 to 0.1.2 (#1272)
[33m9dc982a[m Small changes to favor streamable HTTP over deprecated SSE (#1264)
[33meffde47[m Preparing a pre-release of 0.1.2 (#1260)
[33m04bf831[m docs: fix typos (#1201)
[33m9fd680c[m support streamable http mcp (#1245)
[33m38261fd[m Update Python version requirement and add .cursorrules to .gitignore (#1249)
[33m131f0c7[m feat: add Document Intelligence API version selection via kwargs (#1253)
[33m56f7579[m FIX YouTube transcript errors (#1241)
[33mcb421cf[m Chore: Make linter happy (#1256)
[33m39e7252[m fix: python.lang.security.use-defused-xml-parse.use-defused-xml-parse-packages-markitdown-src-markitdown-converter_utils-docx-math-omml.py (#1251)
[33mbbcf876[m Switched from the stdlib minidom parser to defusedxml. (#1259)
[33m041be54[m Update README.md (#1187)
[33mebe2684[m chore: fix typo in README.md (#1175)
[33m8576f1d[m Add CSV to Markdown table conversion - fixes #1144 (#1176)
[33m3fcd48c[m feat: render math equations in .docx documents (#1160)
[33m9e067c4[m Make it easier to use AzureKeyCredentials with Azure Doc Intelligence (#1151)
[33m9a95105[m Update readme to point to the mcp package. (#1158)
[33m73b9d57[m Update badges (#1157)
[33m3ca5798[m Basic SSE MCP Server for MarkItDown  (#1155)
[33mc1f9a32[m Bump version. (#1154)
[33me928b43[m convert_url renamed to convert_uri, and now handles data and file URIs (#1153)
[33m2ffe6ea[m Bump version. (#1150)
[33mefc55b2[m Bump version and resolve a console encoding error. (#1149)
[33m52432bd[m Add support for preserving base64 encoded images (#1140)
[33mc0a511e[m Updated docx file to include an image. (#1146)
[33mcd6aa41[m Adjust warning filters and update dependencies (#1143)
[33m716f74d[m Consider anything with a charset as plain text-convertible. (#1142)
[33ma93e056[m EPub Support. Adapted #123 to not use epublib. (#1131)
[33mc5f70b9[m Have magika read from the stream. (#1136)
[33m53834fd[m Investigate and silence warnings. (#1133)
[33m5c565b7[m Fix remaining mypy errors. (#1132)
[33ma78857b[m Added epub test file. (#1130)
[33m09df7fe[m Small fixes for autogen integration. (#1124)
[33m6a9f09b[m Updated Magika dependency.
[33m0b815fb[m Bumping version to 0.1.0a2 (#1123)
[33m12620f1[m Handle not supported plot type in pptx (#1122)
[33m5f75e16[m Refactored tests. (#1120)
[33m75140a9[m fix: correct f-string formatting in FileConversionException (#1121)
[33maf1be36[m Added CLI options for extension, mimetypes, and charset. (#1115)
[33m2a2ccc8[m Added mimetypes to _rss_converter
[33m2e51ba2[m Enhance type guessing.
[33m8f8e58c[m Minimize guesses when guesses are compatible. (#1114)
[33m8e73a32[m Switch from puremagic to magika. (#1108)
[33m2405f20[m fix typo in well-known path list (#1109)
[33m99d8e56[m Fix exiftool in well-known paths. (#1106)
[33m515fa85[m feat(docker): improve dockerfile build (#220)
[33m0229ff6[m feat: sort pptx shapes to be parsed in top-to-bottom, left-to-right order (#1104)
[33m82d84e3[m Fixed formatting. (#1098)
[33m36c4bc9[m Fixed deepcopy failure when passing llm_client (#1089)
[33m80baa5d[m fix(README): correct pip install command formatting (#1090)
[33m00a65e8[m Fixed version in README.
[33m6bedf6d[m Fixed version. (#1097)
[33m9380112[m Fixed loading of plugins. (#1096)
[33m784c293[m Bump plugin version.
[33m70e9f8c[m Bump version. (#1094)
[33me921497[m Update converter API, user streams rather than file paths (#1088)
[33m1d2f231[m Fixed property name (#1085)
[33mc5cd659[m Exploring ways to allow Optional dependencies (#1079)
[33mf01c6c5[m Exceptions should subclass Exception not BaseException. (#1082)
[33m43bd79a[m Print and log better exceptions when file conversions fail. (#1080)
[33m9182923[m Don't have ZipConverter accept OOXML files. This will never yield a good result. (#1078)
[33m9a19fdd[m Make sure extensions are unique in MarkItDown's convert methods. (#1076)
[33me82e0c1[m Add Support For PPTX Shape Groups (Fix in code design to not miss out on slide content) (#331)
[33ma394cc7[m fix: Implement retry logic for YouTube transcript fetching and fix URL decoding issue (#1035)
[33ma87fbf0[m add necessary imports (#861)
[33md0ed74f[m Fix UnboundLocalError in MarkItDown._convert (#1038)
[33me4b419b[m Pin Markdownify version. (#1069)
[33mdbdf2c0[m Added CLI tests. (#327)
[33m97eeed5[m Doc Intelligence fixes for refactored code (#325)
[33m935da99[m Added priority argument to all converter constructors. (#324)
[33m5ce85c2[m Fix a typo in sample RTF plugin (#320)
[33m3a5ca22[m Don't generate md links in 'pre' blocks (#322)
[33m4b62506[m Small typo in README.
[33mc73afcf[m Cleanup and refactor, in preparation for plugin support. (#318)
[33m73ba69d[m For csv files mimetypes.guess_type is returning "application/vnd.ms-excel" on windows causing an invalid mime type in plaintextconverter. In reference to issue: https://github.com/microsoft/markitdown/issues/150 (#273)
[33m2a4f7bb[m fix: argparse CLI option ordering, fixes #268 (#290)
[33m7cf5e0b[m feat(pptx): support image description with LLM for pptx files (#306)
[33m3090917[m Typo fixed (#270)
[33m7bea267[m remove leading and trailing \n for HtmlConverter (#262)
[33mbf6a15e[m Kennyzhang/docintel docs (#312)
[33mbfde857[m Add support for conversion via Document Intelligence (#303)
[33mf58a864[m Set exiftool path explicitly. (#267)
[33m265aea2[m Removed the holiday away message from README.md (#266)
[33m05b78e7[m Recognize json as plain text (if no other handlers are present). (#261)
[33m4364072[m If puremagic has no guesses, try again after ltrim. (#260)
[33m731b39e[m Added a test for leading spaces. (#258)
[33m08ed328[m Feature/ Add xls support (#169)
[33md248621[m feat: outlook ".msg" file converter (#196)
[33m4678c8a[m fix(transcription): IS_AUDIO_TRANSCRIPTION_CAPABLE should be iniztialized (#194)
[33m125e206[m docs: update README.md (#182)
[33mf94d099[m feat: enable Git support in devcontainer (#136)
[33mcfd2319[m feat: add version option to markitdown CLI (#172)
[33m7316198[m Bump actions/setup-python from 2 to 5 (#179)
[33m9b69467[m Bump actions/cache from 3 to 4 (#178)
[33m857a2d1[m Update README.md (#180)
[33m1123392[m fix: support -o param to avoid encoding issues (#116)
[33m377a7ea[m Bump actions/checkout from 2 to 4 (#177)
[33mc1a0d3d[m chore: configure Dependabot for GitHub Actions updates (#112)
[33m5276616[m Added support to use Pathlib (#93)
[33m7e6c36c[m docs: add contribution guidelines to README (#176)
[33m52d7308[m refactor(tests): add helper function for tests (#87)
[33me642100[m Merge pull request #160 from sugatoray/support_type_hinting
[33m08a2534[m [feat]: add support for type-hinting for PEP-561
[33m8921fe7[m ignore .vscode folder
[33m613825d[m [feat]: add support for type-hinting for PEP-561
[33m18e3f1d[m Merge pull request #91 from PetrAPConsulting/patch-1
[33mc295dee[m Merge branch 'main' into patch-1
[33mdd87dd5[m Merge pull request #156 from microsoft/afourney-patch-1
[33m535147b[m Added holiday notice.
[33m5c776bd[m Update README.md
[33m423a018[m Merge branch 'main' into patch-1
[33m7147bef[m Merge pull request #130 from sugatoray/update_commandline_help
[33ma5f39d6[m Merge branch 'main' into update_commandline_help
[33m925c449[m Merge pull request #121 from l-lumin/add-project-description
[33mb28f380[m Update README.md
[33mc86287b[m feat: add project description in pyproject.toml
[33m6f3c762[m Merge branch 'main' into update_commandline_help
[33mcb66b35[m Merge pull request #132 from microsoft/gagb-patch-1
[33ma2743a5[m Add downloads badge
[33m2774800[m Merge branch 'update_commandline_help' of https://github.com/sugatoray/markitdown into update_commandline_help
[33m6e1b9a7[m Run precommit
[33m1384e80[m update .gitignore to exclude .vscode folder
[33m356e895[m update formatting with pre-commit
[33mf6e75c4[m Update README.md
[33m8bc1bee[m Merge pull request #129 from finchy/main
[33mf4471d9[m Update README.md
[33m0880073[m Update README.md
[33mbb92962[m Update README.md
[33m233ba67[m Update README.md
[33m46b7f04[m Merge branch 'main' into patch-1
[33m5fc7086[m Run pre-commit
[33m39410d0[m Update CLI helpdoc formatting to allow indentation in code
[33m6e4caac[m Safeguard against path traversal for ZipConverter
[33m224f1df[m Update README.md
[33m1deaba1[m Merge pull request #98 from waterimp/feature/fix-code-comments
[33m09cb048[m Merge branch 'main' into feature/fix-code-comments
[33mb029ae1[m Merge pull request #108 from microsoft/gagb-readme
[33m524aa0d[m Update README.md
[33mde1b54d[m Update README.md
[33m1e7806a[m Simplify
[33m1163aa2[m Merge pull request #106 from microsoft/gagb-patch-1
[33m3bcf2bd[m Update README.md
[33m41a10b9[m Merge pull request #64 from l-lumin/add-devcontainer-config
[33mf1e399e[m Merge branch 'main' into add-devcontainer-config
[33m8b02c0b[m Merge pull request #80 from diya155/main
[33m1dda535[m Merge branch 'main' into main
[33m3622143[m Merge branch 'main' into feature/fix-code-comments
[33m457b623[m Merge branch 'main' into add-devcontainer-config
[33m7900314[m Merge pull request #71 from AumGupta/main
[33m9e546a8[m Merge branch 'main' into main
[33mddf695c[m Merge pull request #97 from Soulter/main
[33m8d5f16e[m Fixed formatting.
[33ma571021[m Merge branch 'main' into main
[33m9add517[m Merge branch 'main' into feature/fix-code-comments
[33m3ce21a4[m Merge pull request #102 from microsoft/bump_version
[33m9518c01[m Bump version.
[33m2250455[m Merge pull request #101 from microsoft/add_deprecation_warnings
[33m95188a4[m Merge main.
[33me69d012[m Merge pull request #100 from microsoft/add_llm_tests
[33m03a7843[m Added deprecation warnings for mlm_* arguments.
[33m248d64e[m Added llm tests to the local test set.
[33m05a49ca[m fix incorrect comments for "bail if not ..." for WAV and image cases.
[33m752fbd3[m feat: add tests of rss convertor
[33m7dc2695[m feat: support convert atom to markdown
[33m53fad6e[m feat: add rss converter
[33mf398f3d[m Update README.md
[33me0a3029[m docs: update README with Devcontainer instructions
[33m07fe457[m feat: add devcontainer configuration and installation script
[33m60c4a62[m Merge branch 'microsoft:main' into main
[33m3eb8cf3[m Merge branch 'main' of https://github.com/AumGupta/markitdown
[33m8c91c11[m pre-commit run
[33m14bd8d3[m Update README.md
[33mad5d4fb[m Merge pull request #77 from microsoft/kevinclb/main
[33mad29122[m run precommit
[33m898bfd4[m Merge branch 'main' into main
[33mc8980d9[m Merge pull request #75 from microsoft/cybernobie/main
[33m24b52b2[m Improve readme
[33m09159aa[m Merge branch 'main' into main
[33m77f620b[m Merge pull request #67 from DIMAX99/issue#65
[33m825d3bb[m Merge branch 'main' into issue#65
[33mc0127af[m Merge pull request #72 from CharlesCNorton/patch-1
[33m33cb501[m Merge branch 'main' into patch-1
[33mcf13b7e[m Merge pull request #73 from CharlesCNorton/patch-2
[33m874eba6[m Merge branch 'main' into patch-2
[33mc3fa293[m Run pre-commit
[33m736e7d9[m Merge branch 'main' into patch-1
[33m19c1112[m Merge pull request #60 from madduci/main
[33m360c2dd[m Merge branch 'main' into main
[33m87846cf[m rm setup.py
[33m33638f1[m feature: add argument parsing and setup.py file for cli tool capability
[33m73776b2[m Merge pull request #50 from narumiruna/youtube-transcript-languages
[33m2d3ffea[m Merge branch 'main' into youtube-transcript-languages
[33m51c1453[m Merge pull request #48 from Soulter/main
[33mae46691[m Merge branch 'main' into main
[33mdbc7276[m Merge branch 'main' into main
[33mb0115cf[m Merge branch 'main' into youtube-transcript-languages
[33m5cf8474[m Merge pull request #44 from Y-Kim-64/main
[33m83dc811[m Merge branch 'main' into main
[33me7a2e20[m Merge pull request #39 from SH4DOW4RE/main
[33m980abd3[m Merge branch 'main' into main
[33mafaff11[m Merge branch 'main' into main
[33m6587e0f[m Merge branch 'main' into patch-1
[33m978c876[m Merge pull request #38 from VillePuuska/support-comments-in-docx
[33me763665[m Merge branch 'main' into support-comments-in-docx
[33mddc1beb[m Merge branch 'main' into patch-2
[33mfa1f496[m Merge branch 'main' into patch-1
[33mda779dd[m Merge pull request #33 from nyosegawa/feature/add-pptx-chart-support
[33m12ce5e9[m Merge branch 'main' into feature/add-pptx-chart-support
[33m6dad1cc[m Merge pull request #22 from Josh-XT/main
[33m9e6a199[m Merge branch 'main' into main
[33med91e8b[m Merge pull request #19 from brc-dd/fix/18
[33maeff2cb[m Merge branch 'main' into fix/18
[33mc9c7d98[m Merge pull request #11 from simonw/patch-2
[33me7d9b55[m Merge branch 'main' into patch-2
[33med651ae[m Fix LLM terminology in code
[33m3d9f3f3[m Fix LLM terms
[33ma3208f2[m feat: Add IpynbConverter
[33mad01da3[m fix issue #65
[33m010f841[m Ensure hatch is installed before running tests
[33m5fc03b6[m Added UID as argument
[33m013b022[m Added Docker Image for using markitdown in a sandboxed environment
[33m695100d[m Support specifying YouTube transcript language
[33md66ef5f[m Update README to introduce the customized mlm_prompt
[33mc168703[m Pass the kwargs to _convert method when converting an url file
[33m3548c96[m Create .gitattributes
[33m1559d9d[m pre-commit ran
[33mb7f5662[m PR: Catching pydub's warning of ffmpeg or avconv missing
[33m0a7203b[m add style_map prop to MarkItDown class
[33m0704b0b[m pass 'style_map' kwarg to mammoth when converting docx
[33m0dd4e95[m Remove _is_chart
[33m93130b5[m Add PPTX chart support
[33m52b7237[m Fix character decoding issues with text-like files
[33ma55c3d5[m Merge branch 'main' into main
[33m81e3f24[m Merge pull request #29 from microsoft/gagb-patch-1
[33mb842946[m Update README.md
[33m60c495d[m Merge branch 'main' into patch-2
[33m71123a4[m Merge pull request #7 from microsoft/gagb/improve-readme
[33m5753e55[m Fix conflicts
[33m752dd89[m Merge pull request #28 from pawarbi/main
[33m1aa4abe[m Merge branch 'gagb/improve-readme' into main
[33mea7c6dc[m Merge pull request #27 from haesleinhuepf/patch-1
[33ma31c0a1[m Merge branch 'main' into gagb/improve-readme
[33m30ab78f[m Update README.md
[33m559b1fc[m Merge branch 'main' into patch-2
[33mdf03382[m Improve docustring
[33m18301ed[m Add installation instructions
[33m4987201[m test
[33m571c5bb[m add test
[33me8ea8b6[m Update readme
[33m7e634ac[m import zipfile
[33m862c390[m add zip handling
[33m70ab149[m Merge pull request #10 from simonw/patch-1
[33m33ce179[m Note about piping
[33m6ebef5a[m CLI usage instructions
[33m3b88696[m Remove invalid classifiers
[33m3f9ba06[m Improve the readme with contributing guidelines
[33mb401396[m Merge pull request #4 from microsoft/fixes_for_filesurfer
[33mcc0a039[m Small fixes for the filesurfer.
[33m851c7cf[m Merge pull request #3 from microsoft/add_cli
[33m2ad821a[m Merge branch 'add_cli' of github.com:microsoft/markitdown into add_cli
[33m2eab564[m Fix continue trying on errors.
[33me3f8cdf[m Merge branch 'main' into add_cli
[33m997c7af[m Added a simple CLI.
[33m8a29572[m Merge pull request #2 from microsoft/update_readme
[33m3354904[m Merge branch 'main' into update_readme
[33mc784125[m Replaced placeholder content in the readme.
[33mfdf1102[m Merge pull request #1 from microsoft/ci_test
[33m1787b83[m Fix remote tests.
[33mfc33491[m Testing CI
[33mf20c964[m Initial commit.
[33m67fec84[m SUPPORT.md committed
[33m9bc7e2b[m SECURITY.md committed
[33m558adf0[m README.md committed
[33mbc978be[m LICENSE committed
[33m1e22c8e[m CODE_OF_CONDUCT.md committed
[33mf454a6d[m Initial commit
