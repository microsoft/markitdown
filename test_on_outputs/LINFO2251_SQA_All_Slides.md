Software Quality Assurance
Organization
Charles Pecheur
Spring 2025
1

Synoptics
LINGI2251 Software Quality Assurance
5 credits, 30h+15h, 2nd quadrimester
INFO2MS and SINF2MS programs
Option: SE&PS
or as elective course
2

Staff
Charles Pecheur
Organization, lectures
Julien Liénard
Labs, assignments
3

Activities
Lectures
Mondays 16h15 BARB 20
≈10 lectures
Labs
Thursdays 10h45 MERC 21
Apply software engineering techniques and tools to
software applications
Not every week, see schedule, starts in S4
Projects
Apply the tools and techniques seen in the lab sessions
3 assignments
4

Evaluation
Assignments : 40%
cannot be re-presented in september !
Oral exam: 60%
covering the lectures
5

References
Course slides
Available on the Moodle website
Recommended textbooks
Mauro Pezzè and Michal Young
Software Testing and Analysis: Process,
Principles, and Techniques
Wiley, 2008
Out of print, available online for free
(http://ix.cs.uoregon.edu/~michal/book)
Norman Fenton and James Bieman
Software Metrics: A Rigorous and Practical
Approach
3rd edition, CRC Press, 2014
6

Contents
• Principles Of Software Quality
• Models Of Software
• Functional Testing
• Structural Testing
• More Testing
• Test Execution
• Program Analysis
• Finite State Analysis
• Software Reliability
• Software Measurement
8

Schedule (tentative)
| LINGI2251 |                |      | Spring 2025      |              |                  |      |
| --------- | -------------- | ---- | ---------------- | ------------ | ---------------- | ---- |
| Starts    | 3/2/2025as of: |      |                  | 10-févr-2025 |                  |      |
|           | Date           | Type | Lectures         |              | Labs             | Dues |
|           |                |      | Mon 16:15 BARB20 |              | Thu 10:45 MERC21 |      |
|           | lun 3/2        | S1   | (no lecture)     |              | (no lecture)     |      |
|           | lun 10/2       | S2   | Organization     |              | (no lecture)     |      |
Principles Of Software Quality
|     | lun 17/2 | S3  | Models Of Software    |     | (no lecture)       |                  |
| --- | -------- | --- | --------------------- | --- | ------------------ | ---------------- |
|     | lun 24/2 | S4  | Functional Testing    |     | Functional testing |                  |
|     | lun 3/3  | S5  | Structural Testing    |     | Structural testing |                  |
|     | lun 10/3 | S6  | More Testing          |     | (no lecture)       | Assignment 1 due |
|     | lun 17/3 | S7  | Test Execution        |     | (no lecture)       |                  |
|     | lun 24/3 | S8  | Program Analysis      |     | Program Analysis   |                  |
|     | lun 31/3 | S9  | Finite State Analysis |     | (no lecture)       |                  |
lun 7/4 S10 Software Measurement: Size Finite State Analysis Assignment 2 due
|     | lun 14/4 | S11     | Software Measurement: Quality |     | (no lecture) |     |
| --- | -------- | ------- | ----------------------------- | --- | ------------ | --- |
|     | lun 21/4 | HOLIDAY | HOLIDAY                       |     | HOLIDAY      |     |
|     | lun 28/4 | HOLIDAY | HOLIDAY                       |     | HOLIDAY      |     |
lun 5/5 S12 Software Reliability (no lecture) Assignment 3 due
9
|     | lun 12/5 | S13 | (no lecture) |     | (no lecture) |     |
| --- | -------- | --- | ------------ | --- | ------------ | --- |

Support
Moodle : LINFO2251
• Slides
• Pointers
• Resources
• Assignment instructions
• Assignment submissions
• Announces
• Forum
Register!
Teams : not used
10

Software Quality Assurance
1 – Principles of Software Quality
Charles Pecheur
1

Principles of Software Quality
What is Software Quality Assurance?
Software Quality
The Software Lifecycle
Software Quality Activities
Principles of Software Analysis
2

WHAT IS SOFTWARE QUALITY
ASSURANCE?
3

Goal of Software Quality Assurance
| Make | good | software! |
| ---- | ---- | --------- |
4

What software?
All sorts of software
• Products, systems, and services
• Stand-alone to embedded to web
• Software-intensive systems
Wide variety, but focus on software
5

Challenges
• Size
Millions of LOC
• Complexity
100s of people
Months, years
• Environmental stress/constraints
Diverse, unanticipated environments
“no silver bullet”…
But Software Quality Engineering helps
Brooks, Fred P. (1986). "No Silver Bullet — Essence and Accident in Software
Engineering"
6

How Successful Have We Been?
Perform tasks more quickly and effectively
Word processing, online shopping, messaging, …
Support advances in medicine, agriculture,
transportation, multimedia education, …
However, software is not without problems
7

How Successful Have We Been?
Tax form processing system (1980–1985)
developed by Sperry Corporation for IRS for $103 M
+ $90 M needed enhancements
+ $40.2 M on interests (refunds not returned on time)
+ $22.3 M in overtime wages
Therac-25 radio-therapy system (1985-1987)
software bug killed several people
Ariane 5 attitude control system (1996)
re-used from Ariane 4
arithmetic overflow leading to rocket destruction
8

Software Quality Engineering
• Software Testing and Analysis
check conformance, find defects
• Software Quality Assurance
idem + inspection, defect prevention, fault tolerance
• Software Quality Engineering
idem + plan, monitor, measure, improve
Software Quality Engineering
Software Quality Assurance
Testing and Analysis
9

SOFTWARE QUALITY
10

What Is Good Software?
The transcendental view:
Quality is an ideal that we thrive to but cannot attain
The user view:
Quality is fitness for purpose, reliability, absence of
defects
The manufacturing view:
Quality is conformance to the process
The product view:
Quality is showing good inherent characteristics
The value-based view:
Quality is how much the customer is willing to pay for it
11

Errors, Faults, Failures
Error:
a mistake in performing some software activities
Fault:
a defect in the product
Failure:
a departure from the system's required behaviour
12

Defects and Quality
Defect :
some problem with the software
= an error, fault or failure
High quality ≈ low defect
Quality problem ≈ defect impact
13

|         | Dealing         |      | with           |          | Defects |
| ------- | --------------- | ---- | -------------- | -------- | ------- |
| Defect  | prevention      |      |                |          |         |
| Prevent | faults          | from | being          | injected |         |
| Error   | blocking, error |      | source removal |          |         |
| Defect  | removal         |      |                |          |         |
| Remove  | faults          |      |                |          |         |
Inspection (find faults), testing (find failures from faults)
| Defect                   | containment |               |             |         |        |
| ------------------------ | ----------- | ------------- | ----------- | ------- | ------ |
| Keep                     | failures    | local, reduce |             | failure | impact |
| Fault-tolerance, failure |             |               | containment |         |        |
14

| Dealing |        | with | Defects |         |         |
| ------- | ------ | ---- | ------- | ------- | ------- |
|         | Defect |      |         | Failure | Failure |
Defect
|     | prevention |     |     | prevention |     |
| --- | ---------- | --- | --- | ---------- | --- |
removal
Containment
15

Quality Perspectives
Consumers Producers
Clients
pay for the software development
Developer
Customers
Users
buy the software
use the software
after it is developed 16

Quality Perspectives
| Consumer | expectations: external |     | qualities |     |
| -------- | ---------------------- | --- | --------- | --- |
good enough for the price
| Dependable: no defects, doing |                        |                | things           | right |
| ----------------------------- | ---------------------- | -------------- | ---------------- | ----- |
| Useful: serves its            |                        | purpose, doing | the right things |       |
| Producer                      | expectations: internal |                | qualities        |       |
good enough for the cost
maintainable, interoperable, modular
17

Quality of the Product
Users judge external characteristics
number and type of failures
Designers judge internal characteristics
number and type of faults
Quality models relate the user's external view
to the developer's internal view
18

10
| Tian: | Software | Quality  | Engineering |        | Slide | (Ch.2) |
| ----- | -------- | -------- | ----------- | ------ | ----- | ------ |
|       |          | Defining | Quality     | in SQE |       |        |
Properties and Perspectives
|     | Quality: | views | and attributes |     |     |     |
| --- | -------- | ----- | -------------- | --- | --- | --- |
•
|     | View       |     | Attribute   |                 |     |     |
| --- | ---------- | --- | ----------- | --------------- | --- | --- |
|     |            |     | Correctness | Other           |     |     |
|     | Customer   |     | Failures:   | Maintainability |     |     |
|     | (external) |     | reliability | Readability     |     |     |
|     |            |     | safety      | Portability     |     |     |
|     |            |     | etc.        | Performance     |     |     |
Installability
|     |            |     |         | Usability,   |     | etc. |
| --- | ---------- | --- | ------- | ------------ | --- | ---- |
|     | Developer  |     | Faults: | Design       |     |      |
|     | (internal) |     | count   | Size         |     |      |
|     |            |     | distr   | Change       |     |      |
|     |            |     | class   | Complexity   |     |      |
|     |            |     | etc.    | presentation |     |      |
control
|     |     |     |     | data, |     | etc. |
| --- | --- | --- | --- | ----- | --- | ---- |
19
|     | SQE | focus: | correctness-related. |     |     |     |
| --- | --- | ------ | -------------------- | --- | --- | --- |
•
| Wiley-IEEE/CS |     | Press, | 2005 |     | Slides | V2 (2007) |
| ------------- | --- | ------ | ---- | --- | ------ | --------- |

Dependability properties
Correctness:
A program is correct if it is consistent with its specification
seldom practical for non-trivial systems
Reliability:
likelihood of correct function for some ``unit'' of behavior
relative to a specification and usage profile
statistical approximation to correctness (100% reliable = correct)
Safety:
preventing hazards
Robustness:
acceptable (degraded) behavior under extreme conditions
22

Example of Dependability Qualities
Correctness, reliability: let
traffic pass according to
correct pattern and central
scheduling
Robustness, safety: Provide
degraded function when
possible; never signal
conflicting greens.
Blinking red / blinking yellow is
better than no lights; no lights
is better than conflicting greens

Relation among Dependability
Qualities
reliable but robust but not
not correct: safe: catastrophic
failures occur failures can occur
rarely
Correct
Reliable
Safe
Robust
correct but not
safe or robust:
safe but not
the
correct:
specification is
annoying
inadequate
failures can
occur
Ch 4, slide 24

ever
You can’t always get what you want
Property
Decision
Pass/Fail
Procedure
Program
Correctness properties are undecidable
the halting problem can be embedded in almost
every property of interest
25

Verification or validation depends on
Validation and Verification Activities
the specification
1 2 3 4 5 6 7 8
Actual Needs and
User Acceptance (alpha, beta test)
Constraints
Example: elevator response
System Test
Unverifiable (but validatable) spec: ... if a user
Integration Test
presses a request button at floor i, an available
elevator must arrive at floor i soon...
Unit/
Component
Verifiable spec: ... if a user presses a request Module Test
Specs
button at floor i, an available elevator must
arrive at floor i within 30 seconds...
(c) 2007 Mauro Pezzè & Michal Young Ch 2, slide 5 (c) 2007 Mauro Pezzè & Michal Young Ch 2, slide 6
Getting what you need ...
weiveR
Delivered
Package
System System
Specifications Integration
Analysis /
Review
Subsystem
Subsystem
Design/Specs
Analysis /
Review
validation
Unit/
Components
verification
User review of external behavior as it is
determined or becomes visible
ever
Getting what you need ...
You can’t always get what you want
Theorem proving:
Perfect verification of Optimistic inaccuracy:
Unbounded effort to • optimistic inaccuracy: we may
arbitrary properties by
verify general Accept programs that do not possess
logical proof or exhaustive accept some programs that do
properties.
testing (Infinite effort)
the property
not possess the property (i.e.,
Property
Model checking:
exit: tmesatiyn gnot detect all
Decidable but possibly
intractable checking of
Pessimviiostliact iinoancsc)u.racy:
Decision simple temporal
Pass/Fail
properties. Reject programs even if they possess
– testing
Procedure Data flow
the property
Program analysis • pessimistic inaccuracy: it is
ex: static analysis
not guaranteed to accept a
Typical testing
Precise analysis of techniques Simplpifrieodgrparmop eervteiens :i f the program
simple syntactic
Reducdeo tehse pdoesgsreesess tohf efr eperodpoemrtfyor
properties.
simplibfyeiinnggt haen aplryozpeedrty to check
CCoorrrreeccttnneessss pprrooppeerrttiieess aarree uunnddeecciiddaabbllee
– automated program analysis
the halting problem can be embedded in almost
techniques
every property of interest Simplified Optimistic • simplified properties: reduce
properties inaccuracy
the degree of freedom for
Pessimistic
simplifying the property to
inaccuracy
check
26
(c) 2007 Mauro Pezzè & Michal Young Ch 2, slide 7 (c) 2007 Mauro Pezzè & Michal Young Ch 2, slide 8

Quality of the Process
Process quality conditions product quality
The development process needs to be modeled
CMM, ISO 9000, SPICE
Modeling will address questions such as
• Where to find a particular kind of fault?
• How to find faults early?
• How to build in fault tolerance?
• What are alternative activities?
27

Business Quality
≠
Business value is not the same as technical value
How measured?
Return on investment (ROI) profit
investment
in money, effort, resources, time, …
28

THE SOFTWARE LIFECYCLE
29

Software Development Process
Requirement
Specification
Design
Coding
Testing
Release
Variations : waterfall, iterative, spiral, agile, XP, …
QA important in all processes
30

Defect
The V-Model
containement
Need Product
Requirements definition Acceptance Testing
System design System testing
D l
a
e
v
f
e o
c m
t Program design Integration testing
e
p
r
r
e t
v c
e e
n Program writing Unit testing f
e
t
i D
o
n
Code
31

Verification and validation
Validation:
does the software system meet the user's real
needs?
are we building the right software?
Verification:
does the software system meet the requirements
specifications?
are we building the software right?
(c) 2007 Mauro Pezzè & Michal
Ch 2, slide 32
Young

Verification and Validation (V&V)
Validation: specifications accurately reflects the customer's
needs
needs ÷ documents, harder
usability testing, user feedback
Verification: application conform to specifications
documents ÷ documents, easier
testing, static analysis, inspection
Validation Verification
33

Verification and Validation
Need Product
Requirements definition System delivery
System design System testing
Program design Integration testing
Program writing Unit testing
Code
34

V&V Techniques
Validation Verification
Walkthroughs Cross-referencing
Readings
Simulation
Interviews
Consistency checks
Reviews
Completeness checks
Checklists
Reachability checks
Formal inspections
(states, transitions)
Modeling
Model checking
Scenarios
Mathematical proofs
Prototypes
Simulation
35

SOFTWARE QUALITY ACTIVITIES
36

Testing
Executed late in development
Generate tests as early as possible
• Tests generated independently from code,
when the specifications are fresh in the mind of
analysts
• The generation of test cases may highlight
inconsistencies and incompleteness of the
corresponding specifications
• tests may be used as compendium of the
specifications by the programmers

Inspection
can be applied to essentially any document
requirements statements
architectural and detailed design documents
test plans and test cases
program source code
may also have secondary benefits
spreading good practices
instilling shared standards of quality.
takes a considerable amount of time
re-inspecting a changed component can be expensive
used primarily
where other techniques are inapplicable
where other techniques do not provide sufficient coverage

Automatic Static Analysis
More limited in applicability
applicable to formal models,
not to natural language documents
Selected when available
substituting machine cycles for human effort
makes them particularly cost-effective

Computer-Aided Verification
Model checking:
exhaustive search of a specification's execution space
applicable to behavior models (e.g. statecharts, Petri nets)
check state conditions, temporal logic, compare models
Theorem proving:
prove
Specifications AND Assumptions IMPLY Requirements
using built-in theories, inference rules, decision procedures
40

Improving the Process
Long lasting errors are common
It is important to structure the process for
Identifying the most critical persistent faults
Tracking them to frequent errors
Adjusting the development and quality processes to
eliminate errors
Feedback mechanisms are the main ingredient
of the quality process for identifying and
removing errors

PRINCIPLES OF SOFTWARE ANALYSIS
42

Software Analysis Principles
General engineering principles:
•
Partition: divide and conquer
•
Visibility: making information accessible
•
Feedback: tuning the development process
| Specific                                                | analysis | and testing | principles: |
| ------------------------------------------------------- | -------- | ----------- | ----------- |
| • Sensitivity: better to fail every time than sometimes |          |             |             |
| • Redundancy: making intentions explicit                |          |             |             |
| • Restriction: making the problem easier                |          |             |             |

Partition:
divide and conquer
Partition complex activities
into simpler tasks
Partition the input space
both structural and functional
test selection criteria
verification techniques:
abstraction

Visibility:
judging status
The ability to measure progress or status
schedule visibility = “Are we ahead or behind schedule?”
quality visibility = “Does quality meet our objectives?”
Involves setting goals that can be assessed
The biggest challenge is early assessment:
specifications, design
Related to observability
Example: Choosing a simple or standard internal data
format to facilitate unit testing

Feedback:
tuning the process
Learning from experience
Each project provides information to improve the
next
Examples
Checklists are built on the basis of past errors
Error taxonomies can help in building better test
selection criteria
Design guidelines can avoid common pitfalls

Sensitivity:
better to fail every time than sometimes
Consistency helps:
Faults that trigger a failure every time will be
detected and fixed sooner and cheaper
Faults that result in rare random failures will be
detected later and more expensively

Redundancy:
making intentions explicit
Redundant checks can increase the capabilities
of catching specific faults early or more
efficiently.
Static type checking + dynamic type checking:
can reveal many type mismatches earlier and more
efficiently.
Validation of requirement specifications +
validation of the final software:
can reveal errors earlier and more efficiently.
Testing + proof of properties: increase confidence

Restriction:
making the problem easier
Suitable restrictions can reduce hard
(unsolvable) problems to simpler (solvable)
problems
Example: checking uninitialized variables vs.
forced variable initialization in Java
Example: checking serializability of transactions vs.
imposed concurrency control protocol
Example: checking dynamic type errors vs. statically
typed languages

Summary
What is Software Quality Assurance?
Software Quality
The Software Lifecycle
Software Quality Activities
Principles of Software Analysis
50

References
| [Ti] | Software Quality Engineering: Testing, Quality  |     |
| ---- | ----------------------------------------------- | --- |
Assurance, and Quantifiable Improvement.  Jeff
Tian. 2005, Wiley-IEEE Computer Society Press.
Ch. 2, 3, 4, 5
| [PY] | M. Pezzè | and Michal Young, Software Testing  |
| ---- | -------- | ----------------------------------- |
and Analysis: Process, Principles, and Techniques,
Wiley, 2008.
Ch. 2, 3, 4
51

Software Quality Assurance
2 – Models of Software
Charles Pecheur
1

Models of Software
Behaviour models
Control flow graphs
Call graphs
Finite state machines
Data models
Def-use pairs
Data and Control Dependence
Data flow analysis
Reaching definitions
2

Models
| Represent | a system, an artifact, a design |     |     |
| --------- | ------------------------------- | --- | --- |
| Analyse   | a system, an artifact, a design |     |     |
•
| Before | the system is | built |     |
| ------ | ------------- | ----- | --- |
•
| Easier | to analyse/check/test than |     | the actual |
| ------ | -------------------------- | --- | ---------- |
system
3

Abstraction
abstract
| The model is |     | an abstraction |     | of the system |     |     |
| ------------ | --- | -------------- | --- | ------------- | --- | --- |
•
| Removes     |     | irrelevant                         | attributes |     | or details |     |
| ----------- | --- | ---------------------------------- | ---------- | --- | ---------- | --- |
| • Preserves |     | (approximate) important attributes |            |     |            |     |
Abstraction function
| from | (attributes |     | of) system to (attributes |     |     | of) model |
| ---- | ----------- | --- | ------------------------- | --- | --- | --------- |
4

Properties of Models
Compact
Depends on how the model will be used: human or
automated?
Predictive
Able to distinguish between good and bad outcomes of
analysis
Different models for different analyses
Semantically meaningful
Interpret analysis results in a way that permits diagnosis of
the causes of failure
Sufficiently general
Able to represent all practical uses in the intended domain of
application
5

BEHAVIOUR MODELS
6

State Model
| Program execution |     |     | =   |     |
| ----------------- | --- | --- | --- | --- |
PC { x=b;
  y=1;
| sequence | of states |     | and transitions | a 2 |
| -------- | --------- | --- | --------------- | --- |
  while (x>0) do {
b 4
    y=y*a;
x 1     x=x-1;
y 8 } }
…
y=y*a;
•
states: control + data
| location + variables, stack, heap |     |     |     | PC  |
| --------------------------------- | --- | --- | --- | --- |
a 2
•
| transitions: |     | actions |     | b 4 |
| ------------ | --- | ------- | --- | --- |
x 1
| ops, instructions |     |     |     | y 16 |
| ----------------- | --- | --- | --- | ---- |
State space
•
| Full (all possible values) |          |       |                 |     |
| -------------------------- | -------- | ----- | --------------- | --- |
| • Reachable                |          | (from | initial states) |     |
| Essentially                | infinite |       |                 |     |
7

Finite State Model
Finite models of program execution
⇒ abstraction
suppresses details of program execution
maps different concrete states to one abstract state
• Execution is coarsened (fewer steps)
• Nondeterminism is introduced
8

|     | Control Flow Graph |     | : Example |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ------------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Example of Control Flow Graph Linear Code Sequence and Jump (LCSJ)
| public static | String collapseNewlines(String | argStr) |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | ------------------------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
public static String collapseNewlines(String argStr) Essentially subpaths of the control flow graph from one
public static String collapseNewlines(String argStr)
{
branch to another
    {
|     |     |  {  |     |     | b2  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        char lacsht a=r alragsStt r=.c haargrASt(t0r.)c;harAt(0);         char last = argStr.charAt(0);
        StringBuffer argBuf = new StringBuffer();
        StringBuffer argBuf = new StringBuffer();
StringBuffer argBuf = new StringBuffer();
|     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     |     | b1  |     |     |     |     |     |
| --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
public static String collapseNewlines(String argStr)
for (int cIdx = 0 ; cIdx < argStr.length(); cIdx++) From Sequence of basic blocs To
        for (int cIdx = 0 ; cIdx < argStr.length(); cIdx++)
|           |     |     | cIdx < argStr.length(); |     | b3  |     |  {                                    |     |     | b2  |     |     |     |     |     |
| --------- | --- | --- | ----------------------- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|         { |     |     |                         |     |     |     |         char last = argStr.charAt(0); |     |     |     |     |     |     |     |     |
{
False True         StringBuffer argBuf = new StringBuffer(); Entry b1 b2 b3 jX
            char ch = argStr.charAt(cIdx);
|     | char ch = argStr.charAt(cIdx); |     |     |     |     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     |     |     |
| --- | ------------------------------ | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
{ b4
            if (ch != '\n' || last != '\n') Entry b1 b2 b3 b4 jT
            char ch = argStr.charAt(cIdx);
if (ch != '\n' || last != '\n')             if (ch != '\n'  b3
|             {        |                |     |     |       |      |     | cIdx < argStr.length(); |       |      |     |     |       |                |     |     |
| -------------------- | -------------- | --- | --- | ----- | ---- | --- | ----------------------- | ----- | ---- | --- | --- | ----- | -------------- | --- | --- |
|                      |                |     |     |       |      |     |                         |       |      |     |     | Entry | b1 b2 b3 b4 b5 |     | jE  |
|                 argB | uf.append(ch); |     |     |       | True |     |                         | False | True |     |     |       |                |     |     |
|                      | {              |     |     | False |      |     | jX                      |       |      |     |     |       |                |     |     |
b4
|                 last = ch; |     |     |  || last != '\n') | b5  |     |     |     | {   |     |     |     |       |                      |     |     |
| -------------------------- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | -------------------- | --- | --- |
|                            |     |     |                   |     |     |     |     |     |     |     |     | Entry | b1 b2 b3 b4 b5 b6 b7 |     | jL  |
argBuf.append(ch);             char ch = argStr.charAt(cIdx);
            }
|           |            |     |     | True                   |              |     |     |             if (ch != '\n'  |            |     |     |     |     |     |     |
| --------- | ---------- | --- | --- | ---------------------- | ------------ | --- | --- | --------------------------- | ---------- | --- | --- | --- | --- | --- | --- |
|         } | last = ch; |     |     | {                      |              | b6  |     |                             | False True |     |     | jX  | b8  |     | ret |
|           |            |     |     |                 argBuf | .append(ch); |     |     |                             |            | jT  |     |     |     |     |     |
|           |            |     |     |                        |              |     |     |  || last != '\n')           | b5         |     |     |     |     |     |     |
|           |            |     |     |                 last   | = ch;        |     |     |                             |            |     |     |     |     |     |     |
}
        return argBuf.toString();             } True jL b3 b4 jT
|       |     |     |     |       |     |     |     | jE  | {   |     |     |     |     |     |     |
| ----- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     } | }   |     |     | False |     |     |     |     |     |     | b6  |     |     |     |     |
                argBuf.append(ch);
|     |                           |     |     |     |         |     |     |     |                             |     |     | jL  | b3 b4 b5       |     | jE  |
| --- | ------------------------- | --- | --- | --- | ------- | --- | --- | --- | --------------------------- | --- | --- | --- | -------------- | --- | --- |
|     |                           |     |     | }   |         | b7  |     |     |                 last  = ch; |     |     |     |                |     |     |
|     | return argBuf.toString(); |     |     |     | cIdx++) |     |     |     |             }               |     |     |     |                |     |     |
|     |                           |     |     |     |         |     |     |     | False                       |     |     | jL  | b3 b4 b5 b6 b7 |     | jL  |
}
|     |     |     |     |     |     |     |     |     | }   |     | b7  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
cIdx++)
b8
return argBuf.toString();
    }
jL
|     |     |     |     |     |     |     |     | return argBuf.toString(); |     | b8  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
9
    }
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 9 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 10
Interprocedural control flow graph Overestimating the calls relation
The static call graph includes calls through dynamic
| •   | Call graphs |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bindings that never occur in execution.
– Nodes represent procedures
public class C {
• Methods
    public static C cFactory(String kind) {
if (kind == "C") return new C();
• C functions if (kind == "S") return new S();
return null;
    }
• ...
    void foo() {
System.out.println("You called the parent's method");
– Edges represent calls relation
    }
    public static void main(String args[]) {
(new A()).check();
    } A.check()
}
class S extends C {
    void foo() {
System.out.println("You called the child's method");
    }
}
class A {
    void check() {
C myC = C.cFactory("S");
|     |     |     |     |     |     |     |     |     |     |     | C.foo() |     | S.foo() | CcFactory(string) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ----------------- | --- |
myC.foo();
    }
}
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 11 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 12

Control Flow Graph
Example of Control Flow Graph Linear Code Sequence and Jump (LCSJ)
Abstraction:
public static String collapseNewlines(String argStr) Essentially subpaths of the control flow graph from one
public static String collapseNewlines(String argStr)
(set of) program locations (PC)
branch to another
    {
|     |     |     |  {  |     |     | b2  |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        char last = argStr.charAt(0); Finite number of locations         char last = argStr.charAt(0);
        StringBuffer argBuf = new StringBuffer();
        StringBuffer argBuf = new StringBuffer();
|     |     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     |     | b1  |     |     |     |     |
| --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
public static String collapseNewlines(String argStr)
Control Flow Graph (CFG)
|     |     |     |     |     |     |     |     |     |     |     |     | From | Sequence of basic blocs |     | To  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ----------------------- | --- | --- |
        for (int cIdx = 0 ; cIdx < argStr.length(); cIdx++)
|     |     |     |     | cIdx < argStr.length(); | b3  |     |     |  {  |     |     | b2  |     |     |     |     |
| --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        {• Nodes = regions of source code          char last = argStr.charAt(0);
False True         StringBuffer argBuf = new StringBuffer(); Entry b1 b2 b3 jX
            char (cbh =a asrigcS trb.clhoarcAkt(csId)x);
        for (int cIdx = 0 ;
|     |     |     |     | {   |     | b4  |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
            if (ch != '\n' || last != '\n') Entry b1 b2 b3 b4 jT
            char ch = argStr.charAt(cIdx);
| •                                           | Edges     | = possibility      | that      |                             |       |     |     |                         |       |      |     |       |                      |     |     |
| ------------------------------------------- | --------- | ------------------ | --------- | --------------------------- | ----- | --- | --- | ----------------------- | ----- | ---- | --- | ----- | -------------------- | --- | --- |
|                                             |           |                    |           |             if (ch != '\n'  |       |     |     |                         |       | b3   |     |       |                      |     |     |
|             {                               |           |                    |           |                             |       |     |     | cIdx < argStr.length(); |       |      |     |       |                      |     |     |
|                                             | e x e c   | u t i o n proceeds | from the  |                             |       |     |     |                         |       |      |     | Entry | b1 b2 b3 b4 b5       |     | jE  |
|                 arg                         | B u f.a p | pe n d (c h);      |           |                             | True  |     |     |                         | False | True |     |       |                      |     |     |
|                                             |           |                    |           |                             | False |     |     | jX                      |       |      |     |       |                      |     |     |
|                 laset =n cdh; of one region |           |                    |           |                             |       |     |     |                         |       |      | b4  |       |                      |     |     |
|                                             |           |                    |           |  || last != '\n')           | b5    |     |     |                         | {     |      |     |       |                      |     |     |
|                                             |           |                    |           |                             |       |     |     |                         |       |      |     | Entry | b1 b2 b3 b4 b5 b6 b7 |     | jL  |
            char ch = argStr.charAt(cIdx);
|             } | to the beginning |     | of another |     |                        |              |     |     |                             |            |     |     |     |     |     |
| ------------- | ---------------- | --- | ---------- | --- | ---------------------- | ------------ | --- | --- | --------------------------- | ---------- | --- | --- | --- | --- | --- |
|               |                  |     |            |     | True                   |              |     |     |             if (ch != '\n'  |            |     |     |     |     |     |
|         }     |                  |     |            |     | {                      |              | b6  |     |                             | False True |     | jX  | b8  |     | ret |
|               |                  |     |            |     |                 argBuf | .append(ch); |     |     |                             |            | jT  |     |     |     |     |
|               |                  |     |            |     |                        |              |     |     |  || last != '\n')           | b5         |     |     |     |     |     |
|               |                  |     |            |     |                 last   | = ch;        |     |     |                             |            |     |     |     |     |     |
        rIentutrnr aar-gpBurfo.tocSetridngu();ral             } True jL b3 b4 jT
(ignore calls)
|       |     |     |     |     |       |     |     |     | jE  | {   |     |     |     |     |     |
| ----- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     } |     |     |     |     | False |     |     |     |     |     | b6  |     |     |     |     |
                argBuf.append(ch);
| May not cover |     | some | flows |     |         |     |     |     |     |                             |     | jL  | b3 b4 b5 |     | jE  |
| ------------- | --- | ---- | ----- | --- | ------- | --- | --- | --- | --- | --------------------------- | --- | --- | -------- | --- | --- |
|               |     |      |       |     | }       |     | b7  |     |     |                 last  = ch; |     |     |          |     |     |
|               |     |      |       |     | cIdx++) |     |     |     |     |             }               |     |     |          |     |     |
e.g. exceptions are not covered
|     |     |     |     |     |     |     |     |     |     | False |     | jL  | b3 b4 b5 b6 b7 |     | jL  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | -------------- | --- | --- |
} b7
cIdx++)
b8
return argBuf.toString();
    }
jL
|     |     |     |     |     |     |     |     |     | return argBuf.toString(); |     | b8  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |
10
    }
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 9 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 10
Interprocedural control flow graph Overestimating the calls relation
The static call graph includes calls through dynamic
| •   | Call graphs |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bindings that never occur in execution.
– Nodes represent procedures
public class C {
|     | •   | Methods |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    public static C cFactory(String kind) {
if (kind == "C") return new C();
|     | •   | C functions |     |     |     |     | if (kind == "S") return new S(); |     |     |     |     |     |     |     |     |
| --- | --- | ----------- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
return null;
    }
|     | •   | ... |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    void foo() {
System.out.println("You called the parent's method");
– Edges represent calls relation
    }
    public static void main(String args[]) {
(new A()).check();
    } A.check()
}
class S extends C {
    void foo() {
System.out.println("You called the child's method");
    }
}
class A {
    void check() {
C myC = C.cFactory("S");
|     |     |     |     |     |     |     |     |     |     |     | C.foo() |     | S.foo() | CcFactory(string) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ----------------- | --- |
myC.foo();
    }
}
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 11 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 12

Basic blocks
Example of Control Flow Graph Linear Code Sequence and Jump (LCSJ)
Basic block:
public static String collapseNewlines(String argStr) Essentially subpaths of the control flow graph from one
public static String collapseNewlines(String argStr)
| maximal |     | program region |     |     |     |     |     |     |     |     | branch to another |     |     |     |     |     |
| ------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- |
    {
|     |     |     |  {  |     |     | b2  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        char last = argStr.charAt(0);         char last = argStr.charAt(0);
        StringBuffer argBuf = new StringBuffer();
| with | a single entry and  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ---- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        StringBuffer argBuf = new StringBuffer();
|     |     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     |     | b1  |     |     |     |     |     |
| --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
public static String collapseNewlines(String argStr)
single exit point
|     |     |     |     |     |     |     |     |     |     |     |     |     | From | Sequence of basic blocs |     | To  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ----------------------- | --- | --- |
        for (int cIdx = 0 ; cIdx < argStr.length(); cIdx++)
|           |     |     |     | cIdx < argStr.length(); | b3  |     |     |  {                                    |     |     | b2  |     |     |     |     |     |
| --------- | --- | --- | --- | ----------------------- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|         { |     |     |     |                         |     |     |     |         char last = argStr.charAt(0); |     |     |     |     |     |     |     |     |
• Often several False True         StringBuffer argBuf = new StringBuffer(); Entry b1 b2 b3 jX
            char ch = argStr.charAt(cIdx);
        for (int cIdx = 0 ;
|     |     |     |     | {   |     | b4  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
            if (ch != '\n' || last != '\n') Entry b1 b2 b3 b4 jT
statements in one block             char ch = argStr.charAt(cIdx);
|                                    |           |     |      |             if (ch != '\n'  |       |     |     |                         |       | b3   |     |     |       |                |     |     |
| ---------------------------------- | --------- | --- | ---- | --------------------------- | ----- | --- | --- | ----------------------- | ----- | ---- | --- | --- | ----- | -------------- | --- | --- |
|             {                      |           |     |      |                             |       |     |     | cIdx < argStr.length(); |       |      |     |     |       |                |     |     |
|                                    |           |     |      |                             |       |     |     |                         |       |      |     |     | Entry | b1 b2 b3 b4 b5 |     | jE  |
|                 argBuf.append(ch); |           |     |      |                             | True  |     |     |                         | False | True |     |     |       |                |     |     |
|                                    |           |     |      |                             | False |     |     | jX                      |       |      |     |     |       |                |     |     |
| •                                  | Sometimes |     | one  |                             |       |     |     |                         |       |      |     |     |       |                |     |     |
b4
|                 last = ch; |     |     |     |  || last != '\n') | b5  |     |     |     | {   |     |     |     |       |                      |     |     |
| -------------------------- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | -------------------- | --- | --- |
|                            |     |     |     |                   |     |     |     |     |     |     |     |     | Entry | b1 b2 b3 b4 b5 b6 b7 |     | jL  |
            char ch = argStr.charAt(cIdx);
            }
|           | statement |     | in several |     | True                   |              |     |     |             if (ch != '\n'  |            |     |     |     |     |     |     |
| --------- | --------- | --- | ---------- | --- | ---------------------- | ------------ | --- | --- | --------------------------- | ---------- | --- | --- | --- | --- | --- | --- |
|         } |           |     |            |     | {                      |              | b6  |     |                             | False True |     |     | jX  | b8  |     | ret |
|           |           |     |            |     |                 argBuf | .append(ch); |     |     |                             |            | jT  |     |     |     |     |     |
|           | blocks    |     |            |     |                        |              |     |     |  || last != '\n')           | b5         |     |     |     |     |     |     |
|           |           |     |            |     |                 last   | = ch;        |     |     |                             |            |     |     |     |     |     |     |
        return argBuf.toString();             } True jL b3 b4 jT
|       |     |     |     |     |       |     |     |     | jE  | {   |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     } |     |     |     |     | False |     |     |     |     |     |     | b6  |     |     |     |     |
as needed by the execution                 argBuf.append(ch);
|     |     |     |     |     |         |     |     |     |     |                       |       |     | jL  | b3 b4 b5 |     | jE  |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --------------------- | ----- | --- | --- | -------- | --- | --- |
|     |     |     |     |     | }       |     | b7  |     |     |                 last  | = ch; |     |     |          |     |     |
|     |     |     |     |     | cIdx++) |     |     |     |     |             }         |       |     |     |          |     |     |
flow
|     |     |     |     |     |     |     |     |     |     | False |     |     | jL  | b3 b4 b5 b6 b7 |     | jL  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | -------------- | --- | --- |
|     |     |     |     |     |     |     |     |     |     | }     |     | b7  |     |                |     |     |
cIdx++)
b8
return argBuf.toString();
    }
jL
|     |     |     |     |     |     |     |     |     | return argBuf.toString(); |     | b8  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
11
    }
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 9 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 10
Interprocedural control flow graph Overestimating the calls relation
The static call graph includes calls through dynamic
| •   | Call graphs |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bindings that never occur in execution.
– Nodes represent procedures
public class C {
|     | • Methods |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    public static C cFactory(String kind) {
if (kind == "C") return new C();
|     | • C functions |     |     |     |     |     | if (kind == "S") return new S(); |     |     |     |     |     |     |     |     |     |
| --- | ------------- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
return null;
    }
|     | • ... |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    void foo() {
System.out.println("You called the parent's method");
– Edges represent calls relation
    }
    public static void main(String args[]) {
(new A()).check();
    } A.check()
}
class S extends C {
    void foo() {
System.out.println("You called the child's method");
    }
}
class A {
    void check() {
C myC = C.cFactory("S");
|     |     |     |     |     |     |     |     |     |     |     |     | C.foo() |     | S.foo() | CcFactory(string) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ----------------- | --- |
myC.foo();
    }
}
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 11 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 12

Linear Code Sequence and Jump
Example of Control Flow Graph Linear Code Sequence and Jump (LCSJ)
Entry
Linear Code Sequence and Jump
public static String collapseNewlines(String argStr) Essentially subpaths of the control flow graph from one
public( sLtaCtiSc AStrJin)g: collapseNewlines(String argStr)
branch to another
    {
| Subpaths | from one branching point  |     |  {  |     | b2  |     |     |     |     |     |     |     |     |     |     |
| -------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        char last = argStr.charAt(0);         char last = argStr.charAt(0);
to another (jumps)         StringBuffer argBuf = new StringBuffer();
        StringBuffer argBuf = new StringBuffer();
|     |     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     | b1  |     |     |     |     |     |
| --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
proceeding to next block is not  public static String collapseNewlines(String argStr)
        for (int cbIdrxa =n c0 h; cinIdgx < argStr.length(); cIdx++) From Sequence of basic blocs To
|           |     |     | cIdx < argStr.length(); |     | b3  |     |  {                                    |     |     | b2  |     |     |     |     |     |
| --------- | --- | --- | ----------------------- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|         { |     |     |                         |     |     |     |         char last = argStr.charAt(0); |     |     |     |     |     |     |     |     |
jX
False True         StringBuffer argBuf = new StringBuffer(); Entry b1 b2 b3 jX
            char ch = argStr.charAt(cIdx);
| From | Sequence of basic blocs | To  |     |     |     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     |     |     |
| ---- | ----------------------- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
{ b4
            if (ch != '\n' || last != '\n') Entry b1 b2 b3 b4 jT
            char ch = argStr.charAt(cIdx);
|                                    |             |     |             if (ch != '\n'  |       |         |     |                         |       | b3   |     |     |       |                      |     |     |
| ---------------------------------- | ----------- | --- | --------------------------- | ----- | ------- | --- | ----------------------- | ----- | ---- | --- | --- | ----- | -------------------- | --- | --- |
|          E   n{ try                | b1 b2 b3    | jX  |                             |       |         |     | cIdx < argStr.length(); |       |      |     |     |       |                      |     |     |
|                                    |             |     |                             |       |         |     |                         |       |      |     |     | Entry | b1 b2 b3 b4 b5       |     | jE  |
|                 argBuf.append(ch); |             |     |                             |       | True jT |     |                         | False | True |     |     |       |                      |     |     |
|                                    |             |     |                             | False |         |     | jX                      |       |      |     |     |       |                      |     |     |
| Entry                              | b1 b2 b3 b4 | jT  |                             |       |         |     |                         |       |      | b4  |     |       |                      |     |     |
|                 last = ch;         |             |     |  || last != '\n')           | b5    |         |     |                         | {     |      |     |     |       |                      |     |     |
|                                    |             |     |                             |       |         |     |                         |       |      |     |     | Entry | b1 b2 b3 b4 b5 b6 b7 |     | jL  |
            char ch = argStr.charAt(cIdx);
|               } |                      |     | jE  |                        |              |     |     |                             |            |     |     |     |     |     |     |
| --------------- | -------------------- | --- | --- | ---------------------- | ------------ | --- | --- | --------------------------- | ---------- | --- | --- | --- | --- | --- | --- |
| E n try         | b1 b2 b3 b4 b5       | jE  |     | True                   |              |     |     |             if (ch != '\n'  |            |     |     |     |     |     |     |
|         }       |                      |     |     | {                      |              | b6  |     |                             | False True |     |     | jX  | b8  |     | ret |
|                 |                      |     |     |                 argBuf | .append(ch); |     |     |                             |            | jT  |     |     |     |     |     |
| Entry           | b1 b2 b3 b4 b5 b6 b7 | jL  |     |                        |              |     |     |  || last != '\n')           | b5         |     |     |     |     |     |     |
|                 |                      |     |     |                 last   | = ch;        |     |     |                             |            |     |     |     |     |     |     |
        return argBuf.toString();             } True jL b3 b4 jT
| jX    | b8  | Return |     |       |     |     |     |     |     |     |     |     |     |     |     |
| ----- | --- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|       |     |        |     |       |     |     |     | jE  | {   |     |     |     |     |     |     |
|     } |     |        |     | False |     |     |     |     |     |     | b6  |     |     |     |     |
                argBuf.append(ch);
|     |       |     |     |     |         |     |     |     |                       |       |     | jL  | b3 b4 b5       |     | jE  |
| --- | ----- | --- | --- | --- | ------- | --- | --- | --- | --------------------- | ----- | --- | --- | -------------- | --- | --- |
|     |       |     |     | }   |         | b7  |     |     |                 last  | = ch; |     |     |                |     |     |
| jL  | b3    | jX  |     |     |         |     |     |     |                       |       |     |     |                |     |     |
|     |       |     |     |     | cIdx++) |     |     |     |             }         |       |     |     |                |     |     |
|     |       |     |     |     | jL      |     |     |     | False                 |       |     | jL  | b3 b4 b5 b6 b7 |     | jL  |
| jL  | b3 b4 | jT  |     |     |         |     |     |     |                       |       |     |     |                |     |     |
|     |       |     |     |     |         |     |     |     | }                     |       | b7  |     |                |     |     |
cIdx++)
b8
return argBuf.toString();
| jL  | b3 b4 b5 | jE  |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    }
jL
|     |                |     |     | Return |     |     |     | return argBuf.toString(); |     | b8  |     |     |     |     |     |
| --- | -------------- | --- | --- | ------ | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
| jL  | b3 b4 b5 b6 b7 | jL  |     |        |     | 12  |     |                           |     |     |     |     |     |     |     |
    }
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 9 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 10
Interprocedural control flow graph Overestimating the calls relation
The static call graph includes calls through dynamic
| • Call graphs |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bindings that never occur in execution.
– Nodes represent procedures
public class C {
• Methods
    public static C cFactory(String kind) {
if (kind == "C") return new C();
• C functions if (kind == "S") return new S();
return null;
    }
• ...
    void foo() {
System.out.println("You called the parent's method");
– Edges represent calls relation
    }
    public static void main(String args[]) {
(new A()).check();
    } A.check()
}
class S extends C {
    void foo() {
System.out.println("You called the child's method");
    }
}
class A {
    void check() {
C myC = C.cFactory("S");
|     |     |     |     |     |     |     |     |     |     |     | C.foo() |     | S.foo() | CcFactory(string) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ----------------- | --- |
myC.foo();
    }
}
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 11 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 12

Call Graphs: Example
public class C {
public static C cFactory(String kind) {
if (kind == "C") return new C();
if (kind == "S") return new S();
return null;
}
void foo() {
System.out.println("You called the parent's
method");
}
public static void main(String args[]) {
(new A()).check();
}
}
A.check()
class S extends C {
void foo() {
System.out.println("You called the child's
method");
}
}
class A {
void check() {
C.foo() S.foo() CcFactory(string)
C myC = C.cFactory("S");
myC.foo();
}
}
13

Call Graphs
Call Graphs:
• Nodes represent
procedures
methods, functions, routines,
...
• Edges represent calls
relation
A.check()
interprocedural control flow
C.foo() S.foo() C.cFactory(string)
14

Over-estimating the call graph
| public class            | C {                              | A.check() may  |         | call C.foo() or S.foo() |       |       |
| ----------------------- | -------------------------------- | -------------- | ------- | ----------------------- | ----- | ----- |
| public                  | static C cFactory(String kind) { |                |         |                         |       |       |
|                         |                                  |                | dynamic | binding                 |       |       |
| if (kind == "C") return | new C();                         |                |         |                         |       |       |
| if (kind == "S") return | new S();                         |                |         |                         |       |       |
| return                  | null;                            |                |         |                         |       |       |
| }                       |                                  | A.check() will |         | actually                | never | call  |
| void foo() {            |                                  |                |         |                         |       |       |
C.foo()
System.out.println("You called the
| parent's method");  |     |     | myC will | always | be an instance of S |     |
| ------------------- | --- | --- | -------- | ------ | ------------------- | --- |
}
| public | static void main(String args[]) {  |     |     |     |     |     |
| ------ | ---------------------------------- | --- | --- | --- | --- | --- |
| (new   | A()).check();                      |     |     |     |     |     |
}
}
A.check()
| class S extends | C {  |     |     |     |     |     |
| --------------- | ---- | --- | --- | --- | --- | --- |
| void foo() {    |      |     |     |     |     |     |
System.out.println("You called the
child's method");
}
}
class A {
| void check() {    |                     |         |     |         |     |                    |
| ----------------- | ------------------- | ------- | --- | ------- | --- | ------------------ |
|                   |                     | C.foo() |     | S.foo() |     | C.cFactory(string) |
| C myC             | = C.cFactory("S");  |         |     |         |     |                    |
myC.foo();
}
}
15

Context-Insensitive Call Graphs
| public class  | Context {           |            |
| ------------- | ------------------- | ---------- |
| public static | void main(String    | args[]) {  |
| Context       | c = new Context();  |            |
main
c.foo(3);
c.bar(17);
}
| void foo(int   | n) {         |     |
| -------------- | ------------ | --- |
| int[]  myArray | = new int[ n | ];  |
C.foo C.bar
depends( myArray, 2) ;
}
| void bar(int   | n) {         |     |
| -------------- | ------------ | --- |
| int[]  myArray | = new int[ n | ];  |
C.depends
depends( myArray, 16) ;
}
| void depends( int[] a, int | n   | ) { |
| -------------------------- | --- | --- |
a[n] = 42;
}
}
16

Context-Sensitive Call Graph
|               |                     |            | Keep   | information about calling |              |      | context     |
| ------------- | ------------------- | ---------- | ------ | ------------------------- | ------------ | ---- | ----------- |
| public class  | Context {           |            |        |                           |              |      |             |
| public static | void main(String    | args[]) {  |        |                           |              |      |             |
|               |                     |            | may    | infer                     | that depends | does | not violate |
| Context       | c = new Context();  |            |        |                           |              |      |             |
|               |                     |            | bounds |                           | of a[..]     |      |             |
c.foo(3);
c.bar(17);
}
main
| void foo(int   | n) {         |     |     |     |     |     |     |
| -------------- | ------------ | --- | --- | --- | --- | --- | --- |
| int[]  myArray | = new int[ n | ];  |     |     |     |     |     |
depends( myArray, 2) ;
}
| void bar(int | n) { |     |     |     |     |     | C.bar(17) |
| ------------ | ---- | --- | --- | --- | --- | --- | --------- |
C.foo(3)
| int[]  myArray | = new int[ n | ];  |     |     |     |     |     |
| -------------- | ------------ | --- | --- | --- | --- | --- | --- |
depends( myArray, 16) ;
}
| void depends( int[] a, int | n   | ) { |     |                      |     |                        |     |
| -------------------------- | --- | --- | --- | -------------------- | --- | ---------------------- | --- |
|                            |     |     |     | C.depends(int[3], 2) |     | C.depends(int[17], 16) |     |
a[n] = 42;
}
}
17

Context-Sensitive Analysis: Growth
The number of contexts grows exponentially
with the depth of the calls
A
1 context A
#C ≈ #P depth
B C
#C number of contexts
2 contexts AB AC
D
E
#P number of procedures
4 contexts ABD ABE ACD ACE
F
G
8 contexts …
H
I
16 contexts …
J
18

Finite State Machines
| Finite | state machine (FSM) |     |     |     |     |
| ------ | ------------------- | --- | --- | --- | --- |
•
| Nodes |     | = states (finite |     | number) |     |
| ----- | --- | ---------------- | --- | ------- | --- |
•
| Edges                  |                   | = transitions |                             |            |           |
| ---------------------- | ----------------- | ------------- | --------------------------- | ---------- | --------- |
| Labelled               |                   | with          | condition, operation, event |            |           |
| input / output : Mealy |                   |               |                             | machine    |           |
| Used                   | as specifications |               |                             | of allowed | behaviour |
19

Contex Insensitive Call graphs Contex Sensitive Call graphs
| public class Context { |     |     |     |     | public class Context { |     |     |     |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    public static void main(String args[]) {     public static void main(String args[]) {
| Context c = new Context(); |     |     |     |     | Context c = new Context(); |     |     |     |     |     |     |      |     |     |     |
| -------------------------- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
| c.foo(3);                  |     |     |     |     | c.foo(3);                  |     |     |     |     |     |     | main |     |     |     |
main
| c.bar(17);            |     |     |     |     | c.bar(17);            |     |     |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     }                 |     |     |     |     |     }                 |     |     |     |     |     |     |     |     |     |     |
|     void foo(int n) { |     |     |     |     |     void foo(int n) { |     |     |     |     |     |     |     |     |     |     |
int[]  myArray = new int[ n ]; int[]  myArray = new int[ n ];
| depends( myArray, 2) ; |     |       |     |       | depends( myArray, 2) ; |     |     |     |     |          |     |     |           |     |     |
| ---------------------- | --- | ----- | --- | ----- | ---------------------- | --- | --- | --- | --- | -------- | --- | --- | --------- | --- | --- |
|     }                  |     | C.foo |     | C.bar |     }                  |     |     |     |     | C.foo(3) |     |     | C.bar(17) |     |     |
|     void bar(int n) {  |     |       |     |       |     void bar(int n) {  |     |     |     |     |          |     |     |           |     |     |
int[]  myArray = new int[ n ]; int[]  myArray = new int[ n ];
| depends( myArray, 16) ; |     |     |           |     | depends( myArray, 16) ; |     |     |     |                       |     |     |                        |     |     |     |
| ----------------------- | --- | --- | --------- | --- | ----------------------- | --- | --- | --- | --------------------- | --- | --- | ---------------------- | --- | --- | --- |
|     }                   |     |     |           |     |     }                   |     |     |     |                       |     |     |                        |     |     |     |
|                         |     |     | C.depends |     |                         |     |     |     | C.depends(int!3),a,2) |     |     | C.depends (int!3),a,2) |     |     |     |
    void depends( int[] a, int n ) {     void depends( int[] a, int n ) {
| a[n] = 42; |     |     |     |     | a[n] = 42; |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     }      |     |     |     |     |     }      |     |     |     |     |     |     |     |     |     |     |
| }          |     |     |     |     | }          |     |     |     |     |     |     |     |     |     |     |
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 13 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 14
|     |     |     |     |     | Finite |     | State Machine: Example |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Context Sensitive CFG
Finite state machines
exponential growth
|     |     |     |     | Transition Diagram |     |     |     |     |     |     | State-Transition Table |     |     |     |     |
| --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- |
• finite set of states (nodes)
A • set of transitions among states (edges)
|     |     |     |     |     | Mealy | machine |     |     |     |     |     | NB: easy | to see | missing |     |
| --- | --- | --- | --- | --- | ----- | ------- | --- | --- | --- | --- | --- | -------- | ------ | ------- | --- |
1 context A Graph representation (Mealy machine) Tatbrualanrs rietpiroesnesntation
B C
|     |     |     |     |     |     |    LF_ |     | Other char |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
apend
emit
   LF_
2 contexts AB AC
emit
D sLtFate x CinRput →EO Fstateo'th /e routput
|     | E   |                            |     |     | e      |      |            | w   |        |     |        |        |     |          |       |
| --- | --- | -------------------------- | --- | --- | ------ | ---- | ---------- | --- | ------ | --- | ------ | ------ | --- | -------- | ----- |
|     |     |                            |     |     |        | Emty |            |     | Within |     |        |        |     |          |       |
|     |     |                            |     |     | buffer |      |            |     | line   |     |        |        |     |          |       |
|     |     |                            |     |     |        |      | Other char |     |        | e   | e/emit | e/emit | d/- | w/append |       |
|     |     | 4 contexts ABD ABE ACD ACE |     |     |        |      | append     |     |        |     |        | LF     | CR  | EOF      | other |
F
|     | G   |     |     |     |     |     |     |     |     | w   | e/emit | e/emit | d/emit | w/append |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------ | ------ | -------- | --- |
Other char
|     |     |     |     |     |     |   CR_  | append |     |  EOF |     |     |        |        |     |          |
| --- | --- | --- | --- | --- | --- | ------ | ------ | --- | ---- | --- | --- | ------ | ------ | --- | -------- |
|     |     |     |     |     | LF  |        |        |     |      |     | e   | e/emit | e/emit | d/- | w/append |
|     |     |     |     |     |     | emit   |        |     | emit |     |     |        |        |     |          |
  CR_
|     |     |     |     |     |     |     |     |     |     | l   | e/- |     | d/- | w/append |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
8 contexts …
emit
H
|     | I   |     |     |     |     |     |     |     |     |     | w   | e/emit | e/emit | d/emit | w/append |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------ | ------ | -------- |
|     |     |     |     |     | l   |     |     | d   |     |     |     |        |        |        |          |
Looking for
Done
optional DOS LF
EOF
|     |     | 16 calling contexts … |     |     |     |     |     |     |     |     | l   | e/- |     | d/- | w/append |
| --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- |
EOF
J
input
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 15 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 16
output
20

Finite State Machine Correctness
Correctness wrt. properties
Satisfies specifications
Invariants, temporal logic
Internal correctness
| Completeness | (all inputs in all states) |     |     |
| ------------ | -------------------------- | --- | --- |
Determinism
Correctness wrt. program
| FSM accurately      | represents | program behavior |     |
| ------------------- | ---------- | ---------------- | --- |
| ≡ program correctly | implements |                  | FSM |
Abstraction
21

Abstraction Function
| Checking | correctness                 | wrt. program |
| -------- | --------------------------- | ------------ |
| abstract | : program state → FSM state |              |
For a program state s, if s –op→ s', then
abstract(s) –op→ abstract(s')   or
abstract(s) –op↛
and   abstract(s) = abstract(s')
22

Abstraction: Example
State variables: atCR, pos
Abstraction:
FSM:
23

DATA MODELS
24

Why Data Flow Models?
Control flow graph, call graph, finite state machines:
represent control, behaviour
We also need to reason about data dependence
Where does this value of x come from?
What would be affected by changing this?
...
Many program analyses use data flow information
Often in combination with control flow
Example: “Taint” analysis to prevent SQL injection attacks
Example: Dataflow test criteria
Example: Compiler optimization
25

Def-Use Pairs
...
...
if (...) {
if (...) {
Definition: x
x = ... ;
gets a value
...
x = ...
}
y = ... + x + ... ;
...
Use: the value of
Def-Use x is extracted
path
y = ... + x + ...
...
26

Def-Use Pairs
| Definition: point |     | where | a variable | gets | a value |
| ----------------- | --- | ----- | ---------- | ---- | ------- |
Variable declaration (often the special value “uninitialized”)
| Variable | initialization |     |     |     |     |
| -------- | -------------- | --- | --- | --- | --- |
Assignment
| Values     | received | by a parameter |                 |     |         |
| ---------- | -------- | -------------- | --------------- | --- | ------- |
| Use: point | where    | a value        | from a variable |     | is used |
Expressions
| Conditional |         | statements |     |     |     |
| ----------- | ------- | ---------- | --- | --- | --- |
| Parameter   | passing |            |     |     |     |
Returns
| Def-use (du) pair: pair |      |         | of points   |     |     |
| ----------------------- | ---- | ------- | ----------- | --- | --- |
| from where              |      | a value | is produced |     |     |
| to where                | that | value   | is used     |     |     |
27

Definition-Clear or Killing
x = ... // A: def x
...
q = ...
Definition: x
x = y; // B: kill x, def x
A
x = ... gets a value
z = ...
y = f(x); // C: use x
...
Definition: x gets
Path A..C is a new value, old
B
not definition-clear x = y value is killed
...
Path B..C is
definition-clear Use: the value of
C
y = f(x)
x is extracted
28

Definition-Clear Path
| Definition-clear  |            |                 | path: is   |             | a path      | from a definition |             |       | to  |
| ----------------- | ---------- | --------------- | ---------- | ----------- | ----------- | ----------------- | ----------- | ----- | --- |
| a use of the same |            |                 |            | variable    | without     |                   | another     |       |     |
| definition        |            | of the variable |            |             | inbetween   |                   |             |       |     |
| A later           | definition |                 |            | of the same |             | variable          | on the path |       |     |
| kills             | the former |                 | definition |             |             |                   |             |       |     |
| A def-use pair    |            |                 | is         | formed      | if and only |                   | if there    | is a  |     |
| definition-clear  |            |                 | path       | between     |             | the definition    |             | and   |     |
the use
29

Def-Use Pairs
| /**  Euclid's |     | algorithm |     | */  |     |
| ------------- | --- | --------- | --- | --- | --- |
| public class  |     | GCD       |     |     |     |
{
| public int |                       | gcd(int         | x, int | y) {        |               |
| ---------- | --------------------- | --------------- | ------ | ----------- | ------------- |
|            | int                   | tmp;            |        | // A: def   | x, y, tmp     |
|            | while                 | (y != 0) {      |        | // B: use y |               |
|            | tmp                   | = x % y;        |        | // C: def   | tmp; use x, y |
|            | x = y;                |                 |        | // D: def   | x; use y      |
|            | y = tmp;              |                 |        | // E: def   | y; use tmp    |
}
|     | return | x;               |     | // F: use x |     |
| --- | ------ | ---------------- | --- | ----------- | --- |
}
|     |     | x          |     | y          | tmp     |
| --- | --- | ---------- | --- | ---------- | ------- |
|     |     | A, B, C    |     | A, B       | C, D, E |
|     |     | A, B, F    |     | A, B, C    |         |
|     |     | D, E, B, C |     | A, B, C, D |         |
|     |     | D, E, B, F |     | E, B       |         |
E, B, C
E, B, C, D
30

Data Dependence Graph
Data dependence graph:
• Nodes: program regions
as in the control flow graph
• Edges: def-use (du) pairs this x value could be
set at block A or D
labelled with the variable name

Data vs Control Dependence
Data dependence: P2 depends on P1 iff
| data values |              | used | in P2 can be defined | in P1 |
| ----------- | ------------ | ---- | -------------------- | ----- |
| P1 is       | a definition |      | point                |       |
| P2 is       | a use point  |      |                      |       |
Control dependence: P2 depends on P1 iff
| P1 controls |                          | whether | P2 executes |     |
| ----------- | ------------------------ | ------- | ----------- | --- |
| P1 is       | an entry/branching point |         |             |     |
| P2 is       | any                      | point   |             |     |
Program dependence: data or control dependence
32

Control Dependence Graph
| /**  Euclid's | algorithm | */  |
| ------------- | --------- | --- |
| public class  | GCD       |     |
{
| public int | gcd(int    | x, int y) { |
| ---------- | ---------- | ----------- |
| int        | tmp;       |             |
| while      | (y != 0) { |             |
tmp = x % y;
x = y;
y = tmp;
}
| return | x;  |     |
| ------ | --- | --- |
}
Control dependence graph:
| •   | Nodes: program | regions |
| --- | -------------- | ------- |
as in the control flow graph
•
Edges: from entry/branching points
to controlled blocks
33

| Control Dependence | vs Control Flow    |            |       |      |
| ------------------ | ------------------ | ---------- | ----- | ---- |
| Control Flow Graph | Control Dependence |            | Graph |      |
|                    | Block D follows    | C but does |       | not  |
depend on C
|     | D and C could | be executed |     | in  |
| --- | ------------- | ----------- | --- | --- |
either order
34

Dominators
In a rooted, directed graph:
| Node M is a dominator |     | of node N iff |     |     |
| --------------------- | --- | ------------- | --- | --- |
every path from the root to N passes through M
| Node M is an immediate |     | dominator | of node N iff |     |
| ---------------------- | --- | --------- | ------------- | --- |
M dominates N and all other dominators of N dominate M
Each node (except the root) has a unique immediate dominator
The immediate dominator relation forms a tree
|     | A   |     | A   |     |
| --- | --- | --- | --- | --- |
B
B
|     | C   | E   | C   | E   |
| --- | --- | --- | --- | --- |
|     |     |     | D   | F   |
|     | D   | F   |     |     |
|     | G   |     | G   |     |
35

Pre- and Post-dominators
Pre-dominators:
CFG
Calculated in the CFG,
A
using the entry node as the root.
B
A pre-dominates C:
To enter to C you have to go through A
C E
Post-dominators:
Calculated in the reverse CFG,
using the exit node as the root.
D F
G post-dominates C:
To exit from C you have to go through G G
36

Dominators: Example
A
A pre-dominates all nodes
CFG
B
A, B, C pre-dominate D
A
B is the immediate pre- C E
dominator of G
D F
B
F does not pre-dominate G
G
C E
G post-dominates all nodes
A
F and G post-dominate E
B
D F
G is the immediate post-
C E
dominator of B
D F
C does not post-dominate B
G
G
37

Post-Domination and
Control Dependence
Consider a node N that is reached on
some but not all execution paths …
There must be some node C such that: C
C has at least two successors
(control flow decision)
… …
C is not post-dominated by N
a successor of C is post-dominated by N
…
IFF N is control-dependent on C
Intuitively: C is the last decision that
N
controls whether N is executed
38

Control Dependence
A
Execution of F is
not inevitable at B
B
Execution of F is
C E
inevitable at E
D F
G
F is control-dependent on B,
the last point at which its
execution was not inevitable
39

Control dependence: Example
| pre-dominator | control-dependent | post-dominator |
| ------------- | ----------------- | -------------- |
40

DATA FLOW ANALYSIS
41

|     | Calculating |     | Def-Use Pairs |     |     |     |     |
| --- | ----------- | --- | ------------- | --- | --- | --- | --- |
Even with loop-free paths, the number of paths in a graph can
be exponentially larger than the number of nodes and edges
| A   | B   | C   | D   | E   | F   | G   | V   |
| --- | --- | --- | --- | --- | --- | --- | --- |
2 paths from A to B, 4 from A to C, 8 from A to D, …,
128 paths from A to V
Do not search every individual path
Summarize the reaching definitions at a node
over all the paths reaching that node
42

Reaching Definition
| Let  v , v | definitions of variable v at points d, e, |     |     |
| ---------- | ----------------------------------------- | --- | --- |
d e
u a point where v is used.
| v reaches | u (v is a reaching definition |     | at u) iff |
| --------- | ----------------------------- | --- | --------- |
| d         | d                             |     |           |
there is at least one control flow path from d to u
d:  v := x
there is no intervening definition of v on the path
… e:  v := y
| v kills v | iff it is on a control path from d |     |     |
| --------- | ---------------------------------- | --- | --- |
| e d       |                                    |     |     |
… …
| (d, u) is a def-use pair of v iff |     | v reaches | u   |
| --------------------------------- | --- | --------- | --- |
d
u:  z := f(v)
43

Data Flow Algorithm
Goal: compute the reaching definitions at node n
Suppose that node p is an immediate predecessor of
node n
If p can assign variable v, then v reaches n.
p p: v := x
We say the definition v is generated at p.
p
If a definition v reaches p,
d
and if v is not redefined at p,
n: …
then v reaches n.
d
Reach(n) = the set of definitions that reach n
ReachOut(n) = the set of definitions that exit n
44

Reaching Definitions: Example
public class GCD {
public int gcd(int x, int y) {
int tmp; // A: def x, y, tmp
Calculate reaching
while (y != 0) { // B: use y
definitions at E in
tmp = x % y; // C: def tmp; use x, y
terms of its
x = y; // D: def x; use y
immediate
y = tmp; // E: def y; use tmp
predecessor D
}
return x; // F: use x
}
ReachOut(D) = (Reach(D) \ {x }) È {x }
A D
Reach(E) = ReachOut(D)
ReachOut(E) = (Reach(E) \ {y }) È {y }
A E
45

Reaching Definitions: Example
public class GCD  {
public int gcd(int x, int y) {
int tmp;               // A: def x, y, tmp
This line has two
|     | while (y != 0) | {     // B: use y |     |
| --- | -------------- | ----------------- | --- |
predecessors:
tmp = x % y;     // C: def tmp; use x, y
Before the loop,
x = y;               // D: def x; use y
end of the loop
y = tmp;           // E: def y; use tmp
}
return x;              // F: use x
}
Reach(B) = ReachOut(A) È
ReachOut(E)
| ReachOut(A) = {x          | , y , tmp | }       |      |
| ------------------------- | --------- | ------- | ---- |
|                           | A A       | A       |      |
| ReachOut(E) = (Reach(E) \ |           | {y }) È | {y } |
|                           |           | A       | E    |
46

Reach Analysis: Equations
È
| Reach(n) =   |     |     | ReachOut(m) |     |     |     |     |
| ------------ | --- | --- | ----------- | --- | --- | --- | --- |
mÎpred(n)
n:  v = …
| ReachOut(n) = (Reach(n) \ |     |        |         | kill (n)) È |     | gen(n) |     |
| ------------------------- | --- | ------ | ------- | ----------- | --- | ------ | --- |
| gen(n) = { v              |     | | v is | defined | or modified |     | at n } |     |
n
| kill(n) = { v |     | | v is | defined | or modified |     | at n, x≠n | }   |
| ------------- | --- | ------ | ------- | ----------- | --- | --------- | --- |
x
| Recursive |       | equations   | for all | nodes | n   |     |     |
| --------- | ----- | ----------- | ------- | ----- | --- | --- | --- |
| Fixed     | point | computation |         |       |     |     |     |
47

Worklist Algorithm for Reach
One way to iterate to a fixed point solution.
| foreach n ∈ nodes { |     |     |     |
| ------------------- | --- | --- | --- |
ReachOut(n) = {} ;
}
worklist = nodes ;
while worklist ≠ {} {
n = choose(worklist) ;
| worklist = worklist \ |     | {n} ; |     |
| --------------------- | --- | ----- | --- |
oldVal = ReachOut(n) ;
| Reach(n) =   | È   | ReachOut(m) ; |     |
| ------------ | --- | ------------- | --- |
mÎpred(n)
| ReachOut(n) = (Reach(n) \ |     | kill (n)) È | gen(n) ; |
| ------------------------- | --- | ----------- | -------- |
| if ReachOut(n) ≠ oldVal   |     | {           |          |
| worklist = worklist È     |     | succ(n) ;   |          |
}
}
48

|          |     |     |     |            |     |     |     |     | public class |       |                              | GCD  {  |        |      |     |           |     |     |
| -------- | --- | --- | --- | ---------- | --- | --- | --- | --- | ------------ | ----- | ---------------------------- | ------- | ------ | ---- | --- | --------- | --- | --- |
| Worklist |     |     |     | algorithm: |     |     |     |     |              |       |                              |         |        |      |     |           |     |     |
|          |     |     |     |            |     |     |     |     | public int   |       | gcd(int                      |         | x, int | y) { |     |           |     |     |
|          |     |     |     |            |     |     |     |     |              | int   | tmp;               // A: def |         |        |      |     | x, y, tmp |     |     |
|          |     |     |     |            |     |     |     |     |              | while | (y != 0) {     // B: use y   |         |        |      |     |           |     |     |
Example
|     |     |     |     |     |     |     |     |     |     | tmp                            |     | = x % y;     // C: def |     |     |     | tmp; use x, y |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | ---------------------- | --- | --- | --- | ------------- | --- | --- |
|     |     |     |     |     |     |     |     |     |     | x = y;               // D: def |     |                        |     |     |     | x; use y      |     |     |
|     |     |     |     |     |     |     |     |     |     | y = tmp;           // E: def   |     |                        |     |     |     | y; use tmp    |     |     |
}
|     |     |     |     |     |     |     |     |     |     | return |     | x;              // F: use x |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --------------------------- | --- | --- | --- | --- | --- | --- |
}
| n   | R = ReachOut(n) |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n
| A   | {x , y  | , tmp | }      |     | x   | , y , tmp |     |        |       |     |      |       |     |     |      |       |     |     |
| --- | ------- | ----- | ------ | --- | --- | --------- | --- | ------ | ----- | --- | ---- | ----- | --- | --- | ---- | ----- | --- | --- |
|     | A       | A     | A      |     | A   | A         | A   |        |       |     |      |       |     |     |      |       |     |     |
| B   | R ∪R    |       |        |     |     |           |     | x , y  | , tmp | , y | …, x |       |     |     | …,   | tmp   |     |     |
|     | A       | E     |        |     |     |           |     | A A    |       | A E |      | D     |     |     |      | C     |     |     |
| C   | R \{tmp |       | }∪{tmp | }   | tmp |           |     |        |       |     | …,   | x , y | , y |     | …, x |       |     |     |
|     | B       |       | _      | C   |     | C         |     |        |       |     |      | A     | A   | E   |      | D     |     |     |
| D   | R \{x   | }∪{x  | }      |     | x   |           |     | …, tmp |       |     |      |       |     |     | …,   | y , y |     |     |
|     | C       | _     | D      |     | D   |           |     |        | C     |     |      |       |     |     |      | A E   |     |     |
}∪{y
| E   | R \{y |     | }   |     | y   |     |     | …, x |     |     | …,  | tmp       |     |     |      |     |        |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --------- | --- | --- | ---- | --- | ------ | --- |
|     | D     | _   | E   |     | E   |     |     | D    |     |     |     |           | C   |     |      |     |        |     |
| F   | R     |     |     |     |     |     |     |      |     |     | x   | , y , tmp |     | , y | …, x |     | …, tmp |     |
|     | B     |     |     |     |     |     |     |      |     |     | A   | A         |     | A E |      | D   |        | C   |
49

|     |     |     | Avail expressions |     |     |
| --- | --- | --- | ----------------- | --- | --- |
Expression exp is available at node n iff for all paths to n, exp has been
| computed |      | and not     | subsequently | modified. |     |
| -------- | ---- | ----------- | ------------ | --------- | --- |
|          | used | in compiler | construction |           |     |
Ç
| Avail | (n) =   | AvailOut(m)  |     |     |     |
| ----- | ------- | ------------ | --- | --- | --- |
mÎpred(n)
(n)) È
| AvailOut(n) = (Avail |     |           | (n) \ kill    | gen(n)   |        |
| -------------------- | --- | --------- | ------------- | -------- | ------ |
| gen(n) = { exp       |     | | exp     | is computed   | at n }   |        |
| kill(n) = { exp      |     | | exp     | has variables | assigned | at n } |
| Recursive            |     | equations |               |          |        |
Worklist algorithm, start with AvailOut(n) = {all expressions}
50

Live variables
A variable v is live at node n iff on some execution path from n,
| v is used | before | it is | changed. |     |
| --------- | ------ | ----- | -------- | --- |
È
| Live(n) =  | LiveOut(m)  |     |     |     |
| ---------- | ----------- | --- | --- | --- |
mÎsucc(n)
| LiveOut(n) = (Live(n) \ |                                       |          | kill (n)) È | gen(n) |
| ----------------------- | ------------------------------------- | -------- | ----------- | ------ |
| gen(n) = { v | v is     |                                       | used     | at n }      |        |
| kill(n) = { v | v is    |                                       | modified | at n        | }      |
| Recursive               | equations                             |          |             |        |
| Worklist                | algorithm, start with LiveOut(n) = {} |          |             |        |
51

Classification of analyses
| Forward/backward: a node’s |     |     | set depends | on that | of its |
| -------------------------- | --- | --- | ----------- | ------- | ------ |
predecessors/successors
Any-path/all-path: a node’s set contains a value iff it is coming
| from any/all | of its | inputs       |       |     |               |
| ------------ | ------ | ------------ | ----- | --- | ------------- |
|              |        | Any-path (È) |       |     | All-paths (Ç) |
| Forward      | (pred) |              | Reach |     | Avail         |
| Backward     | (succ) |              | Live  |     | “inevitable”  |
52

Worklist algorithm
n ∈
| foreach | nodes { |     |     |          |          |        | ⊕ = ∪ |
| ------- | ------- | --- | --- | -------- | -------- | ------ | ----- |
|         |         |     |     | Any-path | :  Xinit | = {},  |       |
X[n] = Xinit ;
⊕
|     |     |     |     | All-path | :  Xinit | = all,  | = ∩ |
| --- | --- | --- | --- | -------- | -------- | ------- | --- |
}
worklist = nodes ;
|     |     |     |     | Forward | :  next | = succ |     |
| --- | --- | --- | --- | ------- | ------- | ------ | --- |
while worklist ≠ {} {
next-1 = prev
n = choose(worklist) ;
| worklist = worklist \ |             | {n} ; |     | Backward | : next | = prev |     |
| --------------------- | ----------- | ----- | --- | -------- | ------ | ------ | --- |
| oldval                | = XOut[n] ; |       |     |          | next-1 | = succ |     |
⊕
| X[n] =              |                       | -1 XOut[m] ; |           |     |     |     |     |
| ------------------- | --------------------- | ------------ | --------- | --- | --- | --- | --- |
|                     | mÎnext                | (n)          |           |     |     |     |     |
| XOut[n] = (X[n] \   |                       | Xkill(n)) È  | Xgen(n) ; |     |     |     |     |
| if XOut[n] ≠ oldVal |                       | {            |           |     |     |     |     |
|                     | worklist = worklist È |              | next(n) ; |     |     |     |     |
}
}
53

Iterative Solution of
Dataflow Equations
Initialize values
For any-path problems: empty set
For all-paths problems: full set
Repeat until nothing changes:
Pick some node and recalculate (new estimate)
Converges on a “fixed point” solution
We can use the same algorithm to approximate other
dynamic properties
Gen set will be “facts that become true here”
Kill set will be “facts that are no longer true here”
Flow equations will describe propagation
54

Arrays and pointers
| Arrays and pointers |              |             | introduce uncertainty:  |                    |        |               |           |          |
| ------------------- | ------------ | ----------- | ----------------------- | ------------------ | ------ | ------------- | --------- | -------- |
| Do different        |              | expressions |                         |                    | access |               | the same  | storage? |
|                     | a[i] same    | as          | a[k] when               | i = k              |        |               |           |          |
|                     | a[i] same    | as          | b[i] when               | a = b (aliasing)   |        |               |           |          |
|                     | *p1 same     | as          | *p2 when                | p1 = p2 (aliasing) |        |               |           |          |
| Any-path: gen       |              |             | sets contains           |                    |        | all           | potential | aliases, |
| kill                | sets contain |             | only                    | what               |        | is definitely |           | modified |
All-path: vice versa
55

Interprocedural Data Flow Analysis
So far: Intraprocedural
Within a single method or procedure
Interprocedural
Across several methods or procedures
Cost/Precision trade-offs are critical, and difficult
context sensitivity
flow sensitivity
56

Context-Sensitive Analysis
foo() {
bar() {
(call)
sub() { (call)
sub()
sub()
}
(return) (return)
} }
A context-sensitive (interprocedural) analysis
distinguishes sub() called from foo()
from sub() called from bar();
A context-insensitive (interprocedural) analysis
does not separate them, as if foo() could call sub()
and sub() could then return to bar()
57

Flow Sensitivity
Reach, Avail, etc. were flow-sensitive,
intraprocedural analyses
O(n3) for one procedure – reasonably cheap
flow-sensitive, interprocedural analyses?
O(n3) on the whole program – prohibitive
Many interprocedural flow analyses are flow-
insensitive
Often is good enough, e.g. type checking
58

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 5, 6
59

Software Quality Assurance
3 – Functional Testing
Charles Pecheur
Feb 2017
1

Functional Testing
Adequacy criteria
Test partition
Combinatorial testing
2

ADEQUACY CRITERIA
3

Testing
| The most | common |     | software quality | assurance  |
| -------- | ------ | --- | ---------------- | ---------- |
technique
The more tests,
| the more dependable |      |                       | the software |            |
| ------------------- | ---- | --------------------- | ------------ | ---------- |
| We want             | each | software module to be |              | thoroughly |
tested
| When is | a suite of tests adequate? |     |     |     |
| ------- | -------------------------- | --- | --- | --- |
4

Adequate Tests
Adequate tests = ?
We wish: If the system passes the tests,
then it must be correct
But that’s impossible!
provably undecidable (halting problem)
We will have to settle for a weaker goal:
Test design rules to highlight inadequacies
5

Test Adequacy Criteria: Examples
Criterion (functional): if the specification describes different
treatment cases, the test suite should check all cases
If the test suite does not check some case, we may conclude that the test
suite is inadequate.
Criterion (structural): the test suite should execute all program
statements
If no test in the test suite executes a particular statement, the test suite is
inadequate.
Some criterion not satisfied ⇒ useful information for improving
All criteria satisfied ⇒ some evidence of test thoroughness
7

Test Terminology
Test case: a set of inputs, execution conditions, and
a pass/fail criterion.
Test suite: a set of test cases.
Test or test execution: the activity of executing test
cases and evaluating their results.
P(0) → 10
P(5) → 42
5 = 42 ?
P(x)
P(-10) → 4
8

Test Terminology
Test case specification: a requirement to be
satisfied by one or more test cases.
Test obligation: a partial test case specification,
requiring some property deemed important to
thorough testing.
All signs of x
x = 0 P(0) → 10
x > 0 P(5) → 42
P(x)
x < 0 P(-10) → 4
9

Adequacy Criterion
Adequacy criterion: a predicate that a áprogram, test suiteñ
pair must satisfy.
Adequacy criterion = set of test obligations
A test suite satisfies an adequacy criterion if
| •         | all the tests succeed (pass)                            |          |
| --------- | ------------------------------------------------------- | -------- |
| •         | every obligation is satisfied by at least one test case |          |
| All signs | of x                                                    | adequate |
x = 0 P(0) → 10
x > 0 P(5) → 42
P(x)
x < 0 P(-10) → 4
10

Infeasible Criterion
Sometimes no test suite can satisfy a criterion for a given
program
Example:
z = x * x;
if (z < 0) {
throw new LogicError(
“z must be positive here!”);
}
No test suite can satisfy statement coverage
Solution: eliminate infeasible test obligations
Undecidable in the general case!
Solution: measure fraction of obligations covered
Coverage = % of obligations covered
11

What Adequacy Criteria?
Functional (black box, specification-based)
Example: test all specified treatment cases
Structural (white or glass box, program-based)
Example: traverse each program loop one or more times
Model-based (design models or derived from code)
Example: exercise all transitions in the model
Fault-based (common faults)
Example: Check for buffer overflow by testing on very
large inputs
12

Comparing Criteria
Distinguish stronger from weaker adequacy criteria
When is criterion is provably stronger than another?
Stronger = gives stronger guarantees
test suites
Criterion A subsumes criterion B iff
for every program P,
sat B wrt P
every test suite satisfying A with respect to P
also satisfies B with respect to P sat A wrt P
Example: Exercising all program branches
subsumes exercising all program statements
13

TEST PARTITION
14

Functional and Structural Testing
Different views of the unit under test:
Functional testing (black box, closed box):
Program content is unknown or ignored
in out
Test input/output behavior
Obligations from functional specifications
Structural testing (white box, clear box):
Program content is visible and observed
Test internal operation
Obligations from program code
15

Functional testing
Deriving test cases from program specifications
Functional specification =
description of intended program behavior
informal textual specs, tables, lists, …
state graphs, scenarios, use cases, UML, …
Need Product
Requirements definition System delivery
| At any stage of testing |     | System testing |
| ----------------------- | --- | -------------- |
System design
| unit, integration,  | Program design | Integration testing |
| ------------------- | -------------- | ------------------- |
system, acceptance
|     | Program writing | Unit testing |
| --- | --------------- | ------------ |
Code
16

Exhaustive Testing?
/** @return the roots of a*x^2 + b*x + c */
public double[] roots(double a, double b, double c) {
…
}
Exhaustive testing: all possible values of a, b, c
Three 64-bit doubles
2192 ≈ 1057 possibilities
Any practical test suite will cover a minuscule portion
of the space!
17

|     |     | Random |     |     | Testing |     |
| --- | --- | ------ | --- | --- | ------- | --- |
public double[] roots(double a, double b, double c) {
…
}
Random testing (uniform):
Pick possible inputs uniformly
Avoids designer bias (same assumptions in program and
tests)
Treats all inputs as equally valuable
b2
| Suppose error |          | when     | –       | 4ac = 0 |           |         |
| ------------- | -------- | -------- | ------- | ------- | --------- | ------- |
| Very          | unlikely | to be    | found   | with    | random    | testing |
| Sparse        | error    | – Needle | in huge |         | haystack! |         |
18

Systematic Testing
public double[] roots(double a, double b, double c) {
…
}
Systematic testing (non-uniform):
Select inputs that are especially valuable
Different classes, limit cases, special values
Example: cases with 0, 1, 2 solutions
Functional testing is systematic testing
19

Purpose of Testing
Estimate the proportion of needles to hay
⇒ sample randomly
But that’s not our goal!
Find needles and remove them from hay
⇒ look systematically
We need to use everything we know about needles
20

Systematic Partition Testing
Failures are sparse in
... but dense in some
Failure (the needles)
the space of possible
parts of the space
No failure inputs ... (7/280 = 2.5%)
systematically test some cases from
each part (2/19 = 10.5 %)
seulav
tupni
elbissop
fo
ecaps
ehT
)kcatsyah
eht(
21

Partition Testing
Partition testing:
Separate the input space into classes whose union is the
entire space
Every class covered by (at least) one test case
(Quasi-partition: the classes may overlap)
Desirable: each fault leads to failures that are dense
(easy to find) in some class
Testing that class will likely reveal the failure
Ideal: all points in some class produce the failure
Testing that class will surely reveal the failure
Seldom guaranteed
22

Specification-Based Partition
Functional testing =
Use the functional specification (formal or
informal) to partition the input space
One class per category of behaviour
One class per boundary between categories
Example: roots(a, b, c)
⇒ cases with 0, 1, 2 solutions
23

|           |     | Early    | Test Design |     |
| --------- | --- | -------- | ----------- | --- |
| Tests can | be  | designed | early       |     |
Need Product
| Based | on specifications |     |     |     |
| ----- | ----------------- | --- | --- | --- |
Requirements definition System delivery
Program code is not necessary
System design System testing
Program design Integration testing
Benefits
Program writing Unit testing
| Can reveal |     | problems | in the specification |     |
| ---------- | --- | -------- | -------------------- | --- |
Code
| Assesses  | testability                |                   |     |                   |
| --------- | -------------------------- | ----------------- | --- | ----------------- |
| Documents |                            | the specification |     |                   |
| Extreme   | programming: the tests are |                   |     | the specification |
24

Functional vs structural test: granularity
Steps: From specification to test cases
levels
• Functional test applies at all granularity levels: • 1. Decompose the specification
– Unit (from module interface spec) – If the specification is large, break it into independently
testable features to be considered in testing
– Integration (from API or subsystem spec)
• 2. Select representatives
– System (from system requirements spec)
– Representative values of each input, or
– Regression (from system requirements + bug history)
– Representative behaviors of a model
• Structural (code-based) test design applies to
– Often simple input/output transformations don’t describe a
relatively small parts of a system: system. We use models in program specification, in program
design, and in test design
– Unit
• 3. Form test specifications
– Integration
– Typically: combinations of input values, or model behaviors
• 4. Produce and execute actual tests
(c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 13 (c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 14
From Specifications to Test Cases
From specification to test cases Simple example: Postal code lookup
1. Decompose the specification
Independently testable features
2. Identify classes of values
Representative values of each input
2b.Derive a model
• Input: ZIP code (5-digit
FSM, grammar, CFG/DFG, … US Postal code)
• Output: List of cities
3. Form test specifications
• What are some
representative values (or
Combinations of input values, or
classes of value) to test?
model behaviors
(c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 15 (c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 16
4. Produce and execute test cases
25

Example: Directory Lookup
Input: Last name
First Name
Faculty
Study Year
Output: List of students
Representative values?
26

Example: Representative Values
Correct;
with 0, 1, many students
Empty
Very long
Control characters
Name: accented letters;
spaces; dashes; apostrophes
Faculty: correct (1-4 letters);
existing; non-existing;
5 letters; non-alphabetical
Study Year: correct (SINF2 MS/G);
existing; non-existing
27

Example: Test Specifications
Combine values for all inputs
Possible tests =
product of sets of values
Tests ⊆ D × D × D × D
First Last Fac Year
Not all of them
Too many
Some may be unfeasible
One for each hazard (e.g. very long; control chars)
Combinatorial: all pairs
28

COMBINATORIAL TESTING
29

Combinatorial Testing: Principles
Identify distinct attributes that can be varied
In the parameters, environment, or configuration
Example:
browser could be “IE” or “Firefox”,
operating system could be “Vista”, “XP”, or “OSX”
Systematically generate combinations to be tested
Example: IE on Vista, IE on XP, Firefox on Vista, Firefox
on OSX, ...
Test cases should be varied and include possible “corner
cases”
30

Combinatorial Testing Approaches
Category-partition testing
(manual) identification of values that characterize the input
(automatic) generation of combinations for test cases
Pairwise testing
systematically test interactions among attributes values with
a relatively small number of test cases
Catalog-based testing
aggregate and synthesize the experience of test designers, to
aid in identifying attribute values
31

Category-Partition Testing
Three steps:
1. Decompose the specification into units,
parameters, categories
2. Identify relevant choices (values) for each
category
3. Introduce constraints
Then (automatically) generate test cases
32

Step 1 – Identify Categories
• Identify independently testable units
• For each unit, identify parameters and
environment elements
• For each parameter, identify categories
(characteristics)
Choosing categories: not a trivial task!
no hard-and-fast rules
reflect test designer's judgment
which classes of values may be treated differently by an
implementation?
33

Step 1 – Identify Categories
Example: Check Configuration
Check Configuration: Check the validity of a computer
configuration. The parameters of check configuration are:
Model: A model identifies a specific product and
determines a set of constraints on available
components. …
Set of components: set of (slot, component) pairs,
corresponding to the required and optional slots of the
model. …
One testable unit: check configuration
Two parameters: model, set of components
34

Step 1 – Identify Categories
Example: Model
Model: A model identifies a specific product and determines
a set of constraints on available components. Models are
characterized by logical slots for components, which may or
may not be implemented by physical slots on a bus. Slots
may be required or optional. Required slots must be
assigned with a suitable component to obtain a legal
configuration, while optional slots may be left empty or
filled depending on the customers' needs
Parameter: Model
Categories:
Model number
Number of required slots for selected model (#SMRS)
Number of optional slots for selected model (#SMOS)
35

Step 1 – Identify Categories
Example: Set of Components
Set of components: set of (slot, component) pairs, corresponding to the
required and optional slots of the model. A component is a choice that
be varied within a model, and which is not designed to be replaced by
the end user. Available components and a default for each slot is
determined by the model. The special value empty is allowed (and may
be the default selection) for optional slots. In addition to being
compatible or incompatible with a particular model and slot, individual
components may be compatible or incompatible with each other.
Parameter: Set of Components
Categories:
Correspondence of components with model slots
Number of required components with selection ¹ empty
Required component selection
Number of optional components with selection ¹ empty
Optional component selection 36

Step 1 – Identify Categories
Example: Set of Components
Set of components: A set of (slot, component) pairs, corresponding to
the required and optional slots of the model. A component is a choice
that can be varied within a model, and which is not designed to be
replaced by the end user. Available components and a default for each
slot is determined by the model. The special value empty is allowed
(and may be the default selection) for optional slots. In addition to being
compatible or incompatible with a particular model and slot, individual
components may be compatible or incompatible with each other.
Environment element: Product database
Number of models in database (#DBM)
Number of components in database (#DBC)
37

Step 2 – Identify choices
Identify classes of values for each category
Ignore interactions between different categories
Boundary value testing
extreme values within a class
extreme
interior
values just outside the class
outside
interior (non-extreme) values
Erroneous condition testing
values outside the normal domain of the program
39

Step 2 – Identify choices
Example: Model
Model number
Malformed
Not in database
Valid
Number of required slots for selected model (#SMRS)
0
1
Many
Number of optional slots for selected model (#SMOS)
0
1
Many
40

Step 2 – Identify choices
Example: Set of Components
Correspondence of selection with Number of optional components
model slots
with non empty selection
Omitted slots
0
Extra slots
< #SMOS
Mismatched slots
= #SMOS
Complete correspondence
Optional component selection
Number of required components
with non empty selection Some defaults
0 All valid
< number required slots ³ 1 incompatible with slots
= number required slots ³ 1 incompatible with another selection
Required component selection ³ 1 incompatible with model
Some defaults ³ 1 not in database
All valid
³ 1 incompatible with slots
³ 1 incompatible with another selection
³ 1 incompatible with model
³ 1 not in database
41

Step 2 – Identify choices
Example: Product Database
Number of models in database (#DBM)
0
1
Many
Number of components in database (#DBC)
0
1
Many
NB: 0 and 1 are unusual (special) values. They might cause
unanticipated behavior alone or in combination with particular
values of other parameters.
42

Step 3 – Introduce Constraints
A combination of values for each category
corresponds to a test case specification
large: product of category sizes
most of which are impossible!
Introduce constraints to
rule out impossible combinations
reduce the size of the test suite if too large
43

| Step              |         | 3 – | Introduce              |      |      | Constraints |     |            |     |
| ----------------- | ------- | --- | ---------------------- | ---- | ---- | ----------- | --- | ---------- | --- |
|                   | Error   |     | and Single Constraints |      |      |             |     |            |     |
| Error constraint: |         |     |                        |      |      |             |     |            |     |
| label choices     |         |     | corresponding          |      |      | to errors   |     | as [error] |     |
| error             | choices |     | tested                 | only | once |             |     |            |     |
Single constraint:
label choices to be tested only once as [single]
same as [error] but for non-error choices
|     |            |     | B1  |     | B2  | B3 [single] |     | B4 [error] |     |
| --- | ---------- | --- | --- | --- | --- | ----------- | --- | ---------- | --- |
|     | A1         |     | X   |     | X   |             | X   |            | X   |
|     | A2         |     | X   |     | X   |             |     |            |     |
|     | A3 [error] |     | X   |     |     |             |     |            |     |
44

Step 3 – Introduce Constraints
Example: Check Configuration
Model number Number of optional components with non
empty selection
Malformed
Not in database 0
Valid < #SMOS
Number of required slots for selected model = #SMOS
(#SMRS)
Optional component selection
0
Some defaults
1
All valid
Many
³1 incompatible with slots
Number of optional slots for selected model
³1 incompatible with another selection
(#SMOS)
³1 incompatible with model
0
³1 not in database
1
Many Number of models in database (#DBM)
Correspondence of selection with model slots 0
Omitted slots 1
Extra slots Many
Mismatched slots
Number of components in database (#DBC)
Complete correspondence
Number of required components with non empty 0
selection 1
0 Many
< number required slots
= number required slots
Required component selection 3×3×3×4×3×6×3×6×3×3 = 314928 test cases
Some defaults
All valid most are unfeasible
³1 incompatible with slots
³1 incompatible with another selection e.g. zero slots and at least one incompatible
³1 incompatible with model
³1 not in database slot
45

| Step |     | 3 – | Introduce | Constraints |
| ---- | --- | --- | --------- | ----------- |
Example: Check Configuration
Model number Number of optional components with non
empty selection
| Malformed              | [error] |     |     |         |
| ---------------------- | ------- | --- | --- | ------- |
| Not in database[error] |         |     |     | 0       |
| Valid                  |         |     |     | < #SMOS |
Number of required slots for selected model
= #SMOS
(#SMRS)
Optional component selection
0
Some defaults
1
All valid
Many
³1 incompatible with slots
Number of optional slots for selected model
³1 incompatible with another selection
(#SMOS)
³1 incompatible with model
0
³1 not in database [error]
1
| Many                                         |         |     | Number of models in database (#DBM) |           |
| -------------------------------------------- | ------- | --- | ----------------------------------- | --------- |
| Correspondence of selection with model slots |         |     |                                     | 0 [error] |
| Omitted slots                                | [error] |     |                                     | 1         |
| Extra slots                                  | [error] |     |                                     | Many      |
Mismatched slots[error]
Number of components in database (#DBC)
Complete correspondence
| Number of required components with non empty |     |         |          | 0 [error] |
| -------------------------------------------- | --- | ------- | -------- | --------- |
| selection                                    |     |         |          | 1         |
| 0                                            |     |         |          | Many      |
| < number required slots                      |     | [error] |          |           |
| = number required slots                      |     | [error] | 11 error | choices   |
Required component selection
Some defaults
All valid 1×3×3×1×1×5×3×5×2×2 + 11
³1 incompatible with slots
| ³1 incompatible with another selection |     |     | = 2711 test cases |     |
| -------------------------------------- | --- | --- | ----------------- | --- |
³1 incompatible with model
| ³1 not in database |     | [error] |     |     |
| ------------------ | --- | ------- | --- | --- |
46

| Step |     | 3 –         | Introduce |             | Constraints |     |     |
| ---- | --- | ----------- | --------- | ----------- | ----------- | --- | --- |
|      |     | If-Property |           | Constraints |             |     |     |
If-Property constraint:
| [property X] |     |     | labels choices of a single category |     |     |     |     |
| ------------ | --- | --- | ----------------------------------- | --- | --- | --- | --- |
[if X] conditions a choice on a property of another
category
|              |              |              |     | B1  | B2  | B3 [if P] | B4 [if Q] |
| ------------ | ------------ | ------------ | --- | --- | --- | --------- | --------- |
|              |              | A1           |     | X   | X   |           |           |
|              | A2 [property |              | P]  | X   | X   | X         |           |
| A3 [property |              | P] [property | Q]  | X   | X   | X         | X         |
47

Step 3 – Introduce Constraints
Example: Check Configuration
Number of required slots for selected model (#SMRS)
0
1 [property RSNE]
Many [property RSNE] [property RSMANY]
Number of required components with non empty selection
0 [if RSNE]
< number required slots [if RSMANY]
= number required slots [if RSMANY]
48

Example: Check configuration
Parameter Component
Parameter Model
Correspondence of selection with model slots
Model number
|                 |         | Omitted slots           | [error] |
| --------------- | ------- | ----------------------- | ------- |
| Malformed       | [error] |                         |         |
|                 |         | Extra slots             | [error] |
| Not in database | [error] |                         |         |
|                 |         | Mismatched slots        | [error] |
| Valid           |         | Complete correspondence |         |
# of required components (selection ¹empty)
Number of required slots for selected model (#SMRS)
| 0   | [single] | 0   | [if RSNE] [error] |
| --- | -------- | --- | ----------------- |
1 [property RSNE] [single]  < number required slots [if RSNE] [error]
|     |     | = number required slots | [if RSMANY] |
| --- | --- | ----------------------- | ----------- |
Many  [property RSNE]  [property RSMANY]
Required component selection
Number of optional slots for selected model (#SMOS)
|     |          | Some defaults | [single] |
| --- | -------- | ------------- | -------- |
| 0   | [single] |               |          |
All valid
| 1   | [property OSNE] [single]  |     |     |
| --- | ------------------------- | --- | --- |
³1 incompatible with slots
Many  [property OSNE] [property OSMANY]
³1 incompatible with another selection
³1 incompatible with model
Environment Product database
|     |     | ³1 not in database | [error] |
| --- | --- | ------------------ | ------- |
Number of models in database (#DBM) # of optional components (selection ¹empty)
0
| 0   | [error]  |          |             |
| --- | -------- | -------- | ----------- |
|     |          | < #SMOS  | [if OSNE]   |
| 1   | [single] |          |             |
|     |          | = #SMOS  | [if OSMANY] |
Many
Optional component selection
Number of components in database (#DBC)
|     |         | Some defaults | [single] |
| --- | ------- | ------------- | -------- |
| 0   | [error] |               |          |
All valid
| 1    | [single] | ³1 incompatible with slots             |     |
| ---- | -------- | -------------------------------------- | --- |
| Many |          | ³1 incompatible with another selection |     |
³1 incompatible with model
69 test cases
|     |     | ³1 not in database | [error] |
| --- | --- | ------------------ | ------- |
49

Next…
Category–partition testing: systematic approach to
Identify characteristics and values
Generate combinations
Test suite size grows very rapidly
with number of categories
even with constraints
Can we use a non-exhaustive approach?
Pairwise testing: all pairs of choices
N-way testing: all N-uples of choices
50

Pairwise Testing
Pairwise combination:
generate combinations that efficiently cover all
pairs (triples,…) of choices
Rationale:
Most failures are triggered by single values or
combinations of a few values.
Covering pairs (triples,…) reduces the number of
test cases, but reveals most faults
51

Example: Display Control
| Display Mode | Language | Fonts | Color | Screen  |
| ------------ | -------- | ----- | ----- | ------- |
size
| full-graphics | English    | Minimal   | Monochrome | Hand-held |
| ------------- | ---------- | --------- | ---------- | --------- |
| text-only     | French     | Standard  | Color-map  | Laptop    |
| limited-      | Spanish    | Document- | 16-bit     | Full-size |
| bandwidth     |            | loaded    |            |           |
|               | Portuguese |           | True-color |           |
Total: 3x4x3x4x3 = 432 test cases
No rationale for constraints
Pairwise: cover all pairs of choices
52

Example: Pairwise Combinations
| Language   | Color      | Display Mode      | Fonts           | Screen Size |
| ---------- | ---------- | ----------------- | --------------- | ----------- |
| English    | Monochrome | Full-graphics     | Minimal         | Hand-held   |
| English    | Color-map  | Text-only         | Standard        | Full-size   |
| English    | 16-bit     | Limited-bandwidth | -               | Full-size   |
| English    | True-color | Text-only         | Document-loaded | Laptop      |
| French     | Monochrome | Limited-bandwidth | Standard        | Laptop      |
| French     | Color-map  | Full-graphics     | Document-loaded | Full-size   |
| French     | 16-bit     | Text-only         | Minimal         | -           |
| French     | True-color | -                 | -               | Hand-held   |
| Spanish    | Monochrome | -                 | Document-loaded | Full-size   |
| Spanish    | Color-map  | Limited-bandwidth | Minimal         | Hand-held   |
| Spanish    | 16-bit     | Full-graphics     | Standard        | Laptop      |
| Spanish    | True-color | Text-only         | -               | Hand-held   |
| Portuguese | Monochrome | Text-only         | -               | -           |
| Portuguese | Color-map  | -                 | Minimal         | Laptop      |
Portuguese 16-bit Limited-bandwidth Document-loaded Hand-held
| Portuguese | True-color | Full-graphics     | Minimal  | Full-size |
| ---------- | ---------- | ----------------- | -------- | --------- |
| Portuguese | True-color | Limited-bandwidth | Standard | Hand-held |
17 test cases
53

| Adding | Constraints |     |     |     |     |
| ------ | ----------- | --- | --- | --- | --- |
Omit illegal combinations
example: color = monochrome not compatible with
screen = laptop | full size
Expressed as patterns
example:
OMIT(*, *, *, Monochrome, Laptop)
OMIT(*, *, *, Monochrome, Full-Size)
Handled by considering the case in separate tables
|           | Mono | C-map | 16-bit | True |     |
| --------- | ---- | ----- | ------ | ---- | --- |
| Handheld  | X    | X     | X      | X    |     |
| Laptop    |      | X     | X      | X    |     |
| Full-size |      | X     | X      | X    | 54  |

|               | Adding | Constraints: Separate |           |            | Tables      |
| ------------- | ------ | --------------------- | --------- | ---------- | ----------- |
| Display Mode  |        | Language              | Fonts     | Color      | Screen size |
| full-graphics |        | English               | Minimal   | Monochrome | Hand-held   |
| text-only     |        | French                | Standard  | Color-map  |             |
| limited-      |        | Spanish               | Document- | 16-bit     |             |
| bandwidth     |        |                       | loaded    |            |             |
|               |        | Portuguese            |           | True-color |             |
| Display Mode  |        | Language              | Fonts     | Color      | Screen size |
| full-graphics |        | English               | Minimal   |            |             |
| text-only     |        | French                | Standard  | Color-map  | Laptop      |
| limited-      |        | Spanish               | Document- | 16-bit     | Full-size   |
| bandwidth     |        |                       | loaded    |            |             |
|               |        | Portuguese            |           | True-color |             |
55

Pairwise Testing: Complexity
| For N categories    |                         | with               | M choices     | each:     |      |      |
| ------------------- | ----------------------- | ------------------ | ------------- | --------- | ---- | ---- |
| All combinations    |                         | = O(MN) test cases |               |           |      |      |
| exponential         | in number               |                    | of categories |           |      |      |
| All pairs = O(M2 ×  |                         | log N) test cases  |               |           |      |      |
| logarithmic         | in number               |                    | of categories |           |      |      |
| Generating          | minimal sets by hand is |                    |               |           | very | hard |
| Efficient heuristic |                         | algorithms         |               | and tools |      | are  |
available
56

Next…
Category–partition testing:
Systematic approach to
(manually) Identify characteristics and values
(automatically) Generate combinations
Constraints to reduce the test suites
Pairwise (or n-way) testing:
Much smaller test suites, even without constraints
We still need:
Help to identify the characteristics and values
Learn from past experience
Catalog-based Testing
57

Catalog-Based Testing: Principles
Deriving value classes requires human judgment
Gathering experience in a systematic collection
Catalogs list important cases for each possible type of variable
Example: for integer variables:
The element immediately preceding the lower bound
The lower bound of the interval
A non-boundary element within the interval
The upper bound of the interval
The element immediately following the upper bound
Benefits:
speed up the test design process
routinize many decisions, better focusing human effort
accelerate training and reduce human error
58

Catalog-Based Testing: Process
Step1:
Analyze the initial specification to identify simple elements:
Pre-conditions
Post-conditions
Definitions
Variables
Operations
Step 2:
Derive a first set of test case specifications from pre-conditions, post-
conditions and definitions
Step 3:
Complete the set of test case specifications using test catalogs
59

Example: cgi_decode
Hello+%22world%22 → Hello "world"
Specification:
Function cgi_decode translates a cgi-encoded string to a
plain ASCII string, reversing the encoding applied by the
common gateway interface (CGI) of most web servers
CGI translates spacesto +, and translates most other
non-alphanumericcharacters to hexadecimal escape
sequences
cgi_decode maps +to spaces, %xy(where xand y
are hexadecimal digits) to the corresponding ASCII
character, and other alphanumeric characters to
themselves
60

Example: input/output
[INPUT] encoded: string of characters (the input CGI sequence)
can contain:
alphanumeric characters
the character +
the substring %xy, where x and y are hexadecimal digits
is terminated by a null character
[OUTPUT] decoded: string of characters (the plain ASCII characters
corresponding to the input CGI sequence)
alphanumeric characters copied into output (in corresponding positions)
blank for each + character in the input
single ASCII character with value xy for each substring %xy
[OUTPUT] return: value cgi_decode returns
0 for success
1 if the input is malformed
61

Step 1 – Identify elements
Pre-conditions: conditions on inputs that must
be true before the execution
validated preconditions: checked by the system
assumed preconditions: assumed by the system
Post-conditions: results of the execution
Variables: elements used for the computation
Operations: main operations on variables and
inputs
Definitions: abbreviations used in the spec
62

|     |     | Step | 1 – | Example |
| --- | --- | ---- | --- | ------- |
PRE 1 (Assumed) input string encoded null-terminated string of
chars
| PRE 2 (Validated) |     | input string encoded |     |     |
| ----------------- | --- | -------------------- | --- | --- |
sequence of CGI items
POST 1 if encoded contains alphanumeric characters, they are copied
to the output string
POST 2 if encoded contains characters +, they are replaced in the
output string by ASCII SPACE characters
POST 3 if encoded contains CGI hexadecimals, they are replaced by
the corresponding ASCII characters
| POST 4 | if encoded | is processed correctly, it returns 0 |     |     |
| ------ | ---------- | ------------------------------------ | --- | --- |
POST 5 if encoded contains a wrong CGI hexadecimal (a substring xy,
where either x or y are absent or are not hexadecimal digits,
| cgi_decode | returns 1 |     |     |     |
| ---------- | --------- | --- | --- | --- |
POST 6 if encoded contains any illegal character, it returns 1
63

Step 1 – Example
VAR 1 encoded: a string of ASCII characters
VAR 2 decoded: a string of ASCII characters
VAR 3 return value: a boolean
DEF 1 hexadecimal characters, in range ['0' .. '9', 'A' .. 'F', 'a' .. 'f']
DEF 2 sequences %xy, where x and y are hexadecimal characters
DEF 3 CGI items as alphanumeric character, or '+', or CGI hexadecimal
OP 1 Scan encoded
64

| Step | 2 – | Derive | first set of test specs |
| ---- | --- | ------ | ----------------------- |
Validated preconditions:
simple precondition (expression without operators):
| • inputs that satisfy the precondition        |     |     |     |
| --------------------------------------------- | --- | --- | --- |
| • inputs that do not satisfy the precondition |     |     |     |
compound precondition (with AND or OR):
•
test different cases (MC/DC)
Assumed precondition:
| • only inputs that satisfy the precondition |     |                    |     |
| ------------------------------------------- | --- | ------------------ | --- |
| Postconditions                              |     | and Definitions :  |     |
| • if given as conditional expressions,      |     |                    |     |
consider conditions like validated preconditions
65

Step 2 – Example
PRE 2 (Validated) the input string encoded is a sequence of CGI items
TC-PRE2-1: encodedis a sequence of CGI items
TC-PRE2-2: encodedis not a sequence of CGI items
POST 1 if encoded contains alphanumeric characters, they are copied in the
output string in the corresponding position
TC-POST1-1: encodedcontains alphanumeric characters
TC-POST1-2: encodeddoes not contain alphanumeric characters
POST 2 if encoded contains characters +, they are replaced in the output
string by ASCII SPACE characters
TC-POST2-1: encodedcontains character +
TC-POST2-2: encodeddoes not contain character +
66

Step 3 – Apply the Catalog
• For each element of the catalog,
apply the catalog entry to all matching specifications
• Delete redundant test cases
Catalog:
Each entry = a kind of element that can occur in a specification
Each entry is associated with a list of generic test case specifications
Example:
catalog entry Boolean
two test case specifications: true, false
Label in/out indicate if applicable only to input, output, both
67

A simple catalog (part I)
Boolean
True in/out
False in/out
Enumeration
Each enumerated value in/out
Some value outside the enumerated set in
Range L ... U
L-1 in
L in/out
A value between L and U in/out
U in/out
U+1 in
Numeric Constant C
C in/out
C –1 in
C+1 in
Any other constant compatible with C in

A simple catalog (part II)
Non-Numeric Constant C
| C                                    |     | in/out |
| ------------------------------------ | --- | ------ |
| Any other constant compatible with C |     | in     |
| Some other compatible value          |     | in     |
Sequence
| Empty                                    |     | in/out |
| ---------------------------------------- | --- | ------ |
| A single element                         |     | in/out |
| More than one element                    |     | in/out |
| Maximum length (if bounded) or very long |     | in/out |
| Longer than maximum length (if bounded)  |     | in     |
| Incorrectly terminated                   |     | in     |
Scan with action on elements P
| P occurs at beginning of sequence  |     | in  |
| ---------------------------------- | --- | --- |
| P occurs in interior of sequence   |     | in  |
| P occurs at end of sequence        |     | in  |
| PP occurs contiguously             |     | in  |
| P does not occur in sequence       |     | in  |
| pP where p is a proper prefix of P |     |     |
in
p
| Proper prefix | occurs at end of sequence | in  |
| ------------- | ------------------------- | --- |

|     |     | Step | 3 – | Example |     |     |
| --- | --- | ---- | --- | ------- | --- | --- |
Range L ... U
| L-1                     |     |     |     |     | in     |     |
| ----------------------- | --- | --- | --- | --- | ------ | --- |
| L                       |     |     |     |     | in/out |     |
| A value between L and U |     |     |     |     | in/out |     |
| U                       |     |     |     |     | in/out |     |
| U+1                     |     |     |     |     | in     |     |
Applies to hexadecimal digits (three ranges):
| '/',  | '0',  | a char in '0'..'9',  |     |     | '9',  | ':' |
| ----- | ----- | -------------------- | --- | --- | ----- | --- |
| '@',  | 'A',  | a char in 'A'..'F',  |     |     | 'F',  | 'G' |
| '}',  | 'a',  | a char in 'a'..'f',  |     |     | 'f',  | 'g' |
15 new test cases for each hexadecimal character
70

Example: Generated Test Cases 1/2
TC-POST2-1: encodedcontains + TC-DEF2-11:encodedcontains %`y'
TC-POST2-2:encodeddoes not contain + TC-DEF2-12: encodedcontains %ay
TC-POST3-2:encodeddoes not contain a CGI- TC-DEF2-13:encodedcontains %xy(xin [b..e])
hexadecimal
TC-DEF2-14: encodedcontains %fy'
TC-POST5-2:encodedterminated with %x
TC-DEF2-15:encodedcontains %gy
TC-VAR1-1:encodedis the empty sequence
TC-DEF2-16:encodedcontains %x/
TC-VAR1-2:encodeda sequence containing a single
TC-DEF2-17: encodedcontains %x0
character
TC-DEF2-18:encodedcontains %xy(yin [1..8])
TC-VAR1-3: encodedis a very long sequence
TC-DEF2-19:encodedcontains %x9
TC-DEF2-1:encodedcontains %/y
TC-DEF2-20:encodedcontains %x:
TC-DEF2-2:encodedcontains %0y
TC-DEF2-21:encodedcontains %x@
TC-DEF2-3: encodedcontains '%xy'(x in [1..8])
TC-DEF2-22:encodedcontains %xA
TC-DEF2-4:encodedcontains '%9y'
TC-DEF2-23:encodedcontains %xy(y in [B..E])
TC-DEF2-5:encodedcontains '%:y'
TC-DEF2-24:encodedcontains %xF
TC-DEF2-6:encodedcontains '%@y‘
TC-DEF2-25:encodedcontains %xG
TC-DEF2-7:encodedcontains '%Ay'
TC-DEF2-26:encodedcontains %x`
TC-DEF2-8:encodedcontains '%xy'(x in [B..E])
TC-DEF2-27:encodedcontains %xa
TC-DEF2-9: encodedcontains '%Fy'
TC-DEF2-28: encodedcontains %xy(y in [b..e])
TC-DEF2-10:encodedcontains '%Gy'
TC-DEF2-29:encodedcontains %xf
71

Example: Generated Test Cases 2/2
TC-DEF2-30:encodedcontains %xg
TC-OP1-1:encodedstarts with an
TC-DEF2-31:encodedterminates with % alphanumeric character
TC-DEF2-32: encodedcontains %xyz TC-OP1-2:encodedstarts with +
TC-DEF3-1:encoded contains / TC-OP1-3:encodedstarts with %xy
TC-DEF3-2:encodedcontains 0 TC-OP1-4:encodedterminates with an
TC-DEF3-3:encodedcontains cin [1..8] alphanumeric character
TC-DEF3-4: encoded contains 9 TC-OP1-5:encodedterminates with +
TC-DEF3-5:encodedcontains : TC-OP1-6:encodedterminated with %xy
TC-DEF3-6:encodedcontains @ TC-OP1-7:encodedcontains two
consecutive alphanumeric characters
TC-DEF3-7: encodedcontains A
TC-OP1-8:encodedcontains ++
TC-DEF3-8: encoded contains c in[B..Y]
TC-OP1-9:encoded contains %xy%zw
TC-DEF3-9:encodedcontains Z
TC-OP1-10:encodedcontains %x%yz
TC-DEF3-10: encodedcontains [
TC-DEF3-11:encodedcontains`
TC-DEF3-12:encodedcontains a
TC-DEF3-13:encodedcontains cin [b..y]
TC-DEF3-14:encodedcontains z
TC-DEF3-15:encodedcontains {
72

What Have We Got?
From category-partition testing:
A(manual) step of identifying categories and choices,
with constraints;
an (automated) step of generating combinations
From catalog-based testing:
Recording and using standard patterns for identifying
significant choices
From pairwise testing:
Systematic generation of smaller test suites
These ideas can be combined
73

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 9, 10, 11
74

Software Quality Assurance
4 – Structural Testing
Charles Pecheur
Mar 2017
1

Structural Testing
Structural testing principles
Control flow testing
Data flow testing
2

STRUCTURAL TESTING PRINCIPLES
3

|     |     |     | 3   | Structural |     | Testing |     | [20 points] |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------- | --- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
Example: The cgi decode() function translates CGI encoding to plain ascii text:
/**
|     |     |     |     | *   | @title | cgi_decode |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
@desc
*
cgi_decode
|     |     |     |     | *   | Translate   | a string |     | from        | the CGI | encoding |      | to plain | ascii     | text |
| --- | --- | --- | --- | --- | ----------- | -------- | --- | ----------- | ------- | -------- | ---- | -------- | --------- | ---- |
|     |     |     |     |     | ’+’ becomes | space,   |     | %xx becomes |         | byte     | with | hex      | value xx, |      |
*
|     |     |     |     | *   | other | alphanumeric |     | characters |     | map | to themselves |     |     |     |
| --- | --- | --- | --- | --- | ----- | ------------ | --- | ---------- | --- | --- | ------------- | --- | --- | --- |
*
|     |     |     |     | *   | returns | 0 for | success, | positive |     | for | erroneous |     | input |     |
| --- | --- | --- | --- | --- | ------- | ----- | -------- | -------- | --- | --- | --------- | --- | ----- | --- |
Only "%xy" (x, y hex
|     |     |     |     |     | 1 = bad | hexadecimal |     | digit |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
*
*/
digits) will execute the  int cgi_decode(char *encoded, char *decoded)
{
|     |     |     |     |     | char | *eptr | = encoded; |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- |
fault
|            |     |               |     |     | char  | *dptr   | = decoded; |         |     |        |        |     |               |     |
| ---------- | --- | ------------- | --- | --- | ----- | ------- | ---------- | ------- | --- | ------ | ------ | --- | ------------- | --- |
|            |     |               |     |     | int   | ok = 0; |            |         |     |        |        |     |               |     |
| Functional |     | test criteria |     |     |       |         |            |         |     |        |        |     |               |     |
|            |     |               |     |     | while | (*eptr) |            | /* loop | to  | end of | string | (’  | 0’ character) | */  |
\
{
| may         | not find | that   |     |     |     |            |         |        |        |      |       |        |          |       |
| ----------- | -------- | ------ | --- | --- | --- | ---------- | ------- | ------ | ------ | ---- | ----- | ------ | -------- | ----- |
|             |          |        |     |     |     | char       | c;      |        |        |      |       |        |          |       |
|             |          |        |     |     |     | c = *eptr; |         |        |        |      |       |        |          |       |
|             |          |        |     |     |     | if (c      | == ’+’) | {      | /* ’+’ | maps | to    | blank  | */       |       |
| Tests would |          | not be |     |     |     |            |         |        |        |      |       |        |          |       |
|             |          |        |     |     |     | *dptr      |         | = ’ ’; |        |      |       |        |          |       |
|             |          |        |     |     |     | } else     | if      | (c ==  | ’%’)   | { /* | ’%xx’ | is hex | for char | xx */ |
adequate
|     |     |     |     |     |     | int | digit_high  |      | =      | Hex_Values[*(++eptr)]; |           |     |        |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---- | ------ | ---------------------- | --------- | --- | ------ | --- |
|     |     |     |     |     |     | int | digit_low   |      | =      | Hex_Values[*(++eptr)]; |           |     |        |     |
|     |     |     |     |     |     | if  | (digit_high |      | ==     | -1 ||                  | digit_low |     | == -1) |     |
|     |     |     |     |     |     |     | ok          | = 1; | /* Bad | return                 | code      | */  |        |     |
6
else
1/6/
|     |     |     |     |     |     |     | *dptr | =   | *   | digit_high |     | + digit_low; |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ---------- | --- | ------------ | --- | --- |
Structural testing
|     |     |     |     |     |     | } else | { /* | All      | other | characters |     | map | to themselves | */  |
| --- | --- | --- | --- | --- | --- | ------ | ---- | -------- | ----- | ---------- | --- | --- | ------------- | --- |
|     |     |     |     |     |     | *dptr  |      | = *eptr; |       |            |     |     |               |     |
}
| requires | that | all parts  |     |     |     |         |         |     |     |     |     |     |     |     |
| -------- | ---- | ---------- | --- | --- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
|          |      |            |     |     |     | ++dptr; | ++eptr; |     |     |     |     |     |     |     |
}
are tested
|     |     |     |     |     | *dptr | = ’ 0’; |     | /* Null | terminator |     | for | string | */  |     |
| --- | --- | --- | --- | --- | ----- | ------- | --- | ------- | ---------- | --- | --- | ------ | --- | --- |
\
|     |     |     |     |     | return | ok; |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
}
a) For each of the following coverage criteria, provide a set of inputs to cgi decode that
|     |     |     |     | achieves |     | 100% coverage: |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | -------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
4
|     |     |     |     | 1.            | [4 points] | Statement |          | coverage  |          |     |     |     |     |     |
| --- | --- | --- | --- | ------------- | ---------- | --------- | -------- | --------- | -------- | --- | --- | --- | --- | --- |
|     |     |     |     | 2.            | [4 points] | Branch    | coverage |           |          |     |     |     |     |     |
|     |     |     |     | 3.            | [4 points] | Branch    | and      | condition | coverage |     |     |     |     |     |
|     |     |     |     | 4.            | [4 points] | MC/DC     | coverage |           |          |     |     |     |     |     |
|     |     |     |     | 5.            | [4 points] | Loop      | boundary | coverage  |          |     |     |     |     |     |
|     |     |     | Use | the following |            | format:   |          |           |          |     |     |     |     |     |
cgi_decode("foo")
cgi_decode("bar")
10

|     |     |     |     |     | 3   | Structural |     | Testing |     | [20 points] |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
Example: The cgi decode() function translates CGI encoding to plain ascii text:
/**
|     |     |     |     |     |     | *   | @title | cgi_decode |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
@desc
*
cgi_decode
|     |     |     |     |     |     | *   | Translate   | a string |     | from        | the CGI | encoding |      | to plain | ascii     | text |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | ----------- | ------- | -------- | ---- | -------- | --------- | ---- |
|     |     |     |     |     |     |     | ’+’ becomes | space,   |     | %xx becomes |         | byte     | with | hex      | value xx, |      |
*
|     |     |     |     |     |     | *   | other | alphanumeric |     | characters |     | map | to themselves |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------------ | --- | ---------- | --- | --- | ------------- | --- | --- | --- |
*
|                     |     |     |     |     |     | *   | returns | 0 for       | success, | positive |     | for | erroneous |     | input |     |
| ------------------- | --- | --- | --- | --- | --- | --- | ------- | ----------- | -------- | -------- | --- | --- | --------- | --- | ----- | --- |
| Structural coverage |     |     |     | may |     |     | 1 = bad | hexadecimal |          | digit    |     |     |           |     |       |     |
*
*/
|        |     |        |     |     |     | int | cgi_decode(char |     |     | *encoded, | char | *decoded) |     |     |     |     |
| ------ | --- | ------ | --- | --- | --- | --- | --------------- | --- | --- | --------- | ---- | --------- | --- | --- | --- | --- |
| not be |     | enough |     |     |     |     |                 |     |     |           |      |           |     |     |     |     |
{
|     |            |                |         |      |     |     | char  | *eptr   | = encoded; |         |     |        |        |     |               |     |
| --- | ---------- | -------------- | ------- | ---- | --- | --- | ----- | ------- | ---------- | ------- | --- | ------ | ------ | --- | ------------- | --- |
|     |            |                |         |      |     |     | char  | *dptr   | = decoded; |         |     |        |        |     |               |     |
|     | "%0y" will |                | execute | the  |     |     | int   | ok = 0; |            |         |     |        |        |     |               |     |
|     |            |                |         |      |     |     | while | (*eptr) |            | /* loop | to  | end of | string | (’  | 0’ character) | */  |
|     | fault      | but not cause  |         |      |     |     |       |         |            |         |     |        |        |     |               |     |
\
{
|     |     |     |     |     |     |     |     | char | c;  |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
failure
|     |     |     |     |     |     |     |     | c = *eptr; |            |        |        |                        |       |        |          |       |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | ------ | ------ | ---------------------- | ----- | ------ | -------- | ----- |
|     |     |     |     |     |     |     |     | if (c      | == ’+’)    | {      | /* ’+’ | maps                   | to    | blank  | */       |       |
|     |     |     |     |     |     |     |     | *dptr      |            | = ’ ’; |        |                        |       |        |          |       |
|     |     |     |     |     |     |     |     | } else     | if         | (c ==  | ’%’)   | { /*                   | ’%xx’ | is hex | for char | xx */ |
|     |     |     |     |     |     |     |     | int        | digit_high |        | =      | Hex_Values[*(++eptr)]; |       |        |          |       |
|     |     |     |     |     |     |     |     | int        | digit_low  |        | =      | Hex_Values[*(++eptr)]; |       |        |          |       |
"%x" at end of string will
|     |     |     |     |     |     |     |     | if  | (digit_high |      | ==     | -1 ||  | digit_low |     | == -1) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---- | ------ | ------ | --------- | --- | ------ | --- |
|     |     |     |     |     |     |     |     |     | ok          | = 1; | /* Bad | return | code      | */  |        |     |
6
|     | read | past | the end of the  |     |     |     |     | else |     |     |     |     |     |     |     |     |
| --- | ---- | ---- | --------------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
1/6/
|     |     |     |     |     |     |     |     |        | *dptr | =   | *     | digit_high |     | + digit_low; |               |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----- | --- | ----- | ---------- | --- | ------------ | ------------- | --- |
|     |     |     |     |     |     |     |     | } else | { /*  | All | other | characters |     | map          | to themselves | */  |
string but not cause
|     |     |     |     |     |     |     |     | *dptr |     | = *eptr; |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | -------- | --- | --- | --- | --- | --- | --- |
}
|     | failure |     |     |     |     |     |     | ++dptr; | ++eptr; |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
}
|     |     |     |     |     |     |     | *dptr | = ’ 0’; |     | /* Null | terminator |     | for | string | */  |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------- | --- | ------- | ---------- | --- | --- | ------ | --- | --- |
\
|     |     |     |     |     |     |     | return | ok; |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
}
a) For each of the following coverage criteria, provide a set of inputs to cgi decode that
|     |     |     |     |     |     | achieves |     | 100% coverage: |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
5
|     |     |     |     |     |     | 1.            | [4 points] | Statement |          | coverage  |          |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------- | ---------- | --------- | -------- | --------- | -------- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | 2.            | [4 points] | Branch    | coverage |           |          |     |     |     |     |     |
|     |     |     |     |     |     | 3.            | [4 points] | Branch    | and      | condition | coverage |     |     |     |     |     |
|     |     |     |     |     |     | 4.            | [4 points] | MC/DC     | coverage |           |          |     |     |     |     |     |
|     |     |     |     |     |     | 5.            | [4 points] | Loop      | boundary | coverage  |          |     |     |     |     |     |
|     |     |     |     |     | Use | the following |            | format:   |          |           |          |     |     |     |     |     |
cgi_decode("foo")
cgi_decode("bar")
10

Functional and Structural Testing
Different views of the unit under test:
Functional testing (black box, closed box):
Program content is unknown or ignored
in out
Test input/output behavior
Obligations from functional specifications
Structural testing (white box, clear box):
Program content is visible and observed
Test internal operation
Obligations from program code
6

Structural testing
Structural testing = test criteria based on the
structure of the program
Still testing product functionality against its
functional specification
Only the measure of thoroughness/adequacy has
changed
7

Why structural testing?
Find what is missing in our test suite
If part of a program is not executed by any test
then faults in that part cannot be exposed
Complements functional testing:
Finds cases that are treated differently
That is exactly what is desired of test cases!
8

Functional and Structural Testing
Structural testing finds cases
not identified from specifications alone
Typical case: a single item of the specification
implemented by multiple parts of the program
Structural testing may miss faults
that would be caught with functional testing
Typical case: missing path faults
9

Structural testing in practice
1. Functional testing based on specifications
2. Measure structural coverage on code
3. Add tests for elements not covered
May be due to:
Differences between specification and implementation
Flaws of the software or its development process
Inadequate functional test suites
Can be automated!
Coverage measurements are convenient progress indicators
10

Structural Coverage
|           | “    | ”   |
| --------- | ---- | --- |
| What's a  | part | ?   |
Typically, control flow elements:
Statements (or CFG nodes)
Branches (or CFG edges)
Conditions, decisions, paths
Also, data flow elements:
Def-Use pairs, paths
11

CONTROL FLOW TESTING
12

Statement testing
Statement coverage:
| Each statement |     | must be executed at least once  |
| -------------- | --- | ------------------------------- |
variant: block (or node) coverage: each CFG node
# executed statements
| Measure:  | C   | =   |
| --------- | --- | --- |
stmt # statements
Rationale: a fault in a statement can only be
revealed by executing the faulty statement
13

Statements or Blocks?
CFG nodes ≠ statements
may represent basic blocks
multiple statements or parts of statements
Difference in granularity, not in concept
100% node coverage ⇔ 100% statement coverage
A test case that improves one will improve the other
14

Example
|     |     | int cgi_decode(char *encoded | , char *decoded | )   |     |     |
| --- | --- | ---------------------------- | --------------- | --- | --- | --- |
A
|     |     |  {char *eptr = encoded | ;   |     |     |     |
| --- | --- | ---------------------- | --- | --- | --- | --- |
|     |     | char *dptr = decoded   | ;   |     |     |     |
int ok = 0;
T = {“”,
0
“test”,
|                         |     |       | while (*eptr) { B |     |     |     |
| ----------------------- | --- | ----- | ----------------- | --- | --- | --- |
| “test+case%1Dadequacy”} |     | False | True              |     |     |     |
|                         |     |       | char c;           | C   |     |     |
= 17/18 = 94% c = *eptr;
C
| stmt |     |     | if (c == '+') {   |     |     |     |
| ---- | --- | --- | ----------------- | --- | --- | --- |
False
True
D
| T = {“good+test%0Dcase%7U”} |     |     |     |     | *dptr = ' '; | E   |
| --------------------------- | --- | --- | --- | --- | ------------ | --- |
 elseif (c == '%') {
| 1   |     |     |     |     | }   |     |
| --- | --- | --- | --- | --- | --- | --- |
C = 18/18 = 100%
False True
stmt
F G
|     |     | else           | int digit_high = Hex_Values[*(++eptr)]; |     |     |     |
| --- | --- | -------------- | --------------------------------------- | --- | --- | --- |
|     |     | *dptr = *eptr; | int digit_low = Hex_Values[*(++eptr)];  |     |     |     |
T = {“%3D”,
|     |     | }   | if (digit_high == -1 || digit_low == -1) { |     |     |     |
| --- | --- | --- | ------------------------------------------ | --- | --- | --- |
2
“%A”,
|        |     |        | False | True    |     |     |
| ------ | --- | ------ | ----- | ------- | --- | --- |
|        |     |        |       | H       | I   |     |
| “a+b”, |     | else { |       | ok = 1; |     |     |
*dptr = 16 * digit_high +  }
“test”}
digit_low;
}
C = 18/18 = 100%
stmt
|     | *dptr = '\0'; | M   | ++dptr; | L   |     |     |
| --- | ------------- | --- | ------- | --- | --- | --- |
|     | return ok;    |     | ++eptr; |     |     |     |
|     | }             |     | }       |     |     |     |
15

Coverage is not size
| T   | = { | “” ,  | “ test | ” ,  “ | test+case%1Dadequacy |     |     |     |     | ” } | 94% |
| --- | --- | ----- | ------ | ------ | -------------------- | --- | --- | --- | --- | --- | --- |
0
|     |     | “                   |     |     |     |     |     |     | ”   |     |      |
| --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
| T   | = { | good+test%0Dcase%7U |     |     |     |     |     |     | }   |     | 100% |
1
|     |     | “   | ” “ |     | ” “ |     | ”   | “    | ”   |     |      |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- |
| T   | = { | %3D | ,   | %A  | ,   | a+b | ,   | test | }   |     | 100% |
2
Coverage   ≠   number of test cases
|     | #(T | ) < #(T | )   | but C |      | (T  | ) > C |      | (T )  |     |     |
| --- | --- | ------- | --- | ----- | ---- | --- | ----- | ---- | ----- | --- | --- |
|     |     | 1       | 0   |       | stmt |     | 1     | stmt | 0     |     |     |
|     | #(T | ) < #(T | )   | but C |      | (T  | ) = C |      | (T )  |     |     |
|     |     | 1       | 2   |       | stmt |     | 1     | stmt | 2     |     |     |
Minimizing test suite size is seldom the goal
small test cases make failure diagnosis easier
16

Statement coverage can miss cases
|     |     | int cgi_decode(char *encoded |     |     |     | , char *decoded |     | )   |     |     |
| --- | --- | ---------------------------- | --- | --- | --- | --------------- | --- | --- | --- | --- |
Suppose block F were
|         |     |     |  {char *eptr = encoded |     |     | ;   | A   |     |     |     |
| ------- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
| missing |     |     | char *dptr = decoded   |     |     | ;   |     |     |     |     |
int ok = 0;
|                     |     |     |     |     | while (*eptr) { |      | B   |     |     |     |
| ------------------- | --- | --- | --- | --- | --------------- | ---- | --- | --- | --- | --- |
| Statement coverage  |     |     |     |     |                 | True |     |     |     |     |
False
char c;
C
does not require
c = *eptr;
if (c == '+') {
branch from D to L
|     |     |     |                      |     | False |     |     | True |              |     |
| --- | --- | --- | -------------------- | --- | ----- | --- | --- | ---- | ------------ | --- |
|     |     |     |  elseif (c == '%') { |     |       | D   |     |      | *dptr = ' '; | E   |
}
|     |     |        |     | False |                                         | True |     |     |     |     |
| --- | --- | ------ | --- | ----- | --------------------------------------- | ---- | --- | --- | --- | --- |
|     |     | else { |     | F     | int digit_high = Hex_Values[*(++eptr)]; |      |     |     | G   |     |
T = {“”,
|     |     | *dptr = *eptr; |     |     | int digit_low = Hex_Values[*(++eptr)]; |     |     |     |     |     |
| --- | --- | -------------- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- |
3
|     |     | }   |     |     | if (digit_high == -1 || digit_low == -1) { |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
“+%0D+%4J”}
|     |     |     |     |     |     | False |     | True |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | ---- | --- | --- |
C = 17/17 = 100%
ok = 1;
|     |     |     |     | else { |     |     | H   |     | I   |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
stmt
|     |     |     |     | *dptr = 16 * digit_high +  |     |     | }   |     |     |     |
| --- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- |
digit_low;
}
L
|     | *dptr = '\0'; | M   |     |     | ++dptr; |     |     |     |     |     |
| --- | ------------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
++eptr;
return ok;
|     | }   |     |     |     | }   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
17

Branch testing
Branch coverage:
Each branch must be executed at least once
variant: edge coverage: each edge in the CFG
# executed branches
Measure: C =
branch # branches
18

Example
|     |     |     |     | int cgi_decode(char *encoded |     |     | , char *decoded | )   |
| --- | --- | --- | --- | ---------------------------- | --- | --- | --------------- | --- |
A
|     |     |     |     |  {char *eptr = encoded |                      |     | ;   |     |
| --- | --- | --- | --- | ---------------------- | -------------------- | --- | --- | --- |
|     |     |     |     |                        | char *dptr = decoded |     | ;   |     |
int ok = 0;
| T = { | “” ,  | “ +%0D+%4J | ” }  |     |     |     |     |     |
| ----- | ----- | ---------- | ---- | --- | --- | --- | --- | --- |
3
|     |        |     |     |     |       | while (*eptr) { | B    |     |
| --- | ------ | --- | --- | --- | ----- | --------------- | ---- | --- |
| C   | = 100% |     |     |     |       |                 |      |     |
|     |        |     |     |     | False |                 | True |     |
stmt
|     |             |     |     |     |     | char c; |     | C   |
| --- | ----------- | --- | --- | --- | --- | ------- | --- | --- |
| C   | = 88% (7/8) |     |     |     |     |         |     |     |
c = *eptr;
branch
if (c == '+') {
False
True
D
*dptr = ' '; E
 elseif (c == '%') {
}
|       |     |     |     |     | False |     | True |     |
| ----- | --- | --- | --- | --- | ----- | --- | ---- | --- |
|       | “   | ”   |     |     |       |     |      |     |
| T = { | %3D | ,   |     |     |       |     |      |     |
F G
| 2   |     |     |     | else           |     | int digit_high = Hex_Values[*(++eptr)];    |       |      |
| --- | --- | --- | --- | -------------- | --- | ------------------------------------------ | ----- | ---- |
| “   | ”   |     |     | *dptr = *eptr; |     | int digit_low = Hex_Values[*(++eptr)];     |       |      |
| %A  | ,   |     |     |                |     |                                            |       |      |
|     |     |     |     | }              |     | if (digit_high == -1 || digit_low == -1) { |       |      |
| “   | ”   |     |     |                |     |                                            |       |      |
| a+b | ,   |     |     |                |     |                                            | False | True |
H I
|        |     |     |     |     | else {                     |     |     | ok = 1; |
| ------ | --- | --- | --- | --- | -------------------------- | --- | --- | ------- |
| “ test | ” } |     |     |     | *dptr = 16 * digit_high +  |     |     | }       |
digit_low;
}
| C   | = 100% |     |     |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- |
stmt
| C   | = 100% (8/8)  |     |               |     |     |         |     |     |
| --- | ------------- | --- | ------------- | --- | --- | ------- | --- | --- |
|     |               |     | *dptr = '\0'; | M   |     | ++dptr; |     | L   |
branch
|     |     |     | return ok; |     |     | ++eptr; |     |     |
| --- | --- | --- | ---------- | --- | --- | ------- | --- | --- |
|     |     |     | }          |     |     | }       |     |     |
19

Statements vs branches
In a graph:
| Traversing all edges ⇒              | visiting all nodes |          |
| ----------------------------------- | ------------------ | -------- |
| 100% branch coverage ⇒              | 100% stmt          | coverage |
| But the converse is not true (see T | )                  |          |
3
20

Branch coverage can miss cases
|     |     |     |     |     |     | int cgi_decode(char *encoded |     |     |     | , char *decoded |     | )   |     |
| --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --------------- | --- | --- | --- |
A
| Fault: Missing operator (-) |     |     |     |     |     |     |  {char *eptr = encoded |     |     | ;   |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- |
|                             |     |     |     |     |     |     | char *dptr = decoded   |     |     | ;   |     |     |     |
int ok = 0;
|     | digit_high |     | == 1 | ||  |     |     |     |     |     |     |     |     |     |
| --- | ---------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
B
|     |     | digit_low | == -1 |     |     |     |       |     | while (*eptr) { |     |     |     |     |
| --- | --- | --------- | ----- | --- | --- | --- | ----- | --- | --------------- | --- | --- | --- | --- |
|     |     |           |       |     |     |     | False |     | True            |     |     |     |     |
|     |     |           |       |     |     |     |       |     | char c;         |     | C   |     |     |
c = *eptr;
| T   | = {“good+test%0Dcase%7U”} |     |     |     |     |     |     |     | if (c == '+') {   |     |     |     |     |
| --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- |
1
False
| C   | = 100% |     |     |     |     |     |     |     |     |     |     | True |     |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
stmt
D
*dptr = ' '; E
| C      | =   | 100% (8/8) |     |     |     |      |  elseif (c == '%') { |       |                                         |      |     |     |     |
| ------ | --- | ---------- | --- | --- | --- | ---- | -------------------- | ----- | --------------------------------------- | ---- | --- | --- | --- |
| branch |     |            |     |     |     |      |                      |       |                                         |      |     |     | }   |
|        |     |            |     |     |     |      |                      | False |                                         | True |     |     |     |
|        |     |            |     |     |     | else |                      | F     | int digit_high = Hex_Values[*(++eptr)]; |      |     |     | G   |
All branches tested
|     |     |     |     |     |     | *dptr = *eptr; |     |     | int digit_low = Hex_Values[*(++eptr)]; |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------- | --- | --- | -------------------------------------- | --- | --- | --- | --- |
if (digit_high == -/1 || digit_low == -1) {
}
All tests pass
1
|     |     |     |     |     |     |     |     |     |     | False | True |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ---- | --- | --- |
Fault not detected!
|     |     |     |     |     |     |     |     | else {                     |     |     | H ok = 1; |     | I   |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --------- | --- | --- |
|     |     |     |     |     |     |     |     | *dptr = 16 * digit_high +  |     |     | }         |     |     |
digit_low;
}
| The false |     | branch in G |     |     |     |     |     |     |     |     |     |     |     |
| --------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
has two cases
|     |     |     |     |     | *dptr = '\0'; | M   |     |     | ++dptr; |     | L   |     |     |
| --- | --- | --- | --- | --- | ------------- | --- | --- | --- | ------- | --- | --- | --- | --- |
|     |     |     |     |     | return ok;    |     |     |     | ++eptr; |     |     |     |     |
|     |     |     |     |     | }             |     |     |     | }       |     |     |     |     |
21

Condition testing
Branch coverage = decision coverage:
Each decision must be true and false at least once
decision = top-level Boolean expression (condition)
Covers the decomposition of programs into cases
intuitively attractive: check the programmer's case analysis
but only roughly: groups cases with the same outcome
Condition coverage considers case analysis in more detail
individual conditions in a Boolean decision
e.g., both parts of digit_high == 1 || digit_low == -1
22

Basic condition testing
Basic condition coverage:
| Each basic condition must be true |     |     |     |     | and false | at  |
| --------------------------------- | --- | --- | --- | --- | --------- | --- |
least once
|           |     | # executed   |     | true  | basic | conds |
| --------- | --- | ------------ | --- | ----- | ----- | ----- |
|           |     | + # executed |     | false | basic | conds |
| Measure:  | C   | =            |     |       |       |       |
bcond
|     |     |     | 2 # | basic | conds |     |
| --- | --- | --- | --- | ----- | ----- | --- |
×
23

Example
|     | int cgi_decode(char *encoded | , char *decoded | )   |
| --- | ---------------------------- | --------------- | --- |
A
|     |  {char *eptr = encoded | ;   |     |
| --- | ---------------------- | --- | --- |
|     | char *dptr = decoded   | ;   |     |
5 basic conditions int ok = 0;
|     |     | while (*eptr) { B |     |
| --- | --- | ----------------- | --- |
B, C, D, 2 × G
|     | False | True    |     |
| --- | ----- | ------- | --- |
|     |       | char c; | C   |
c = *eptr;
= {“good+test%0Dcase%7U”} if (c == '+') {
T
1 False
True
C = 8/8 = 100%
D
*dptr = ' '; E
branch  elseif (c == '%') {
}
C = 9/10 = 90%
bcond
False True
F G
|     | else           | int digit_high = Hex_Values[*(++eptr)];    |      |
| --- | -------------- | ------------------------------------------ | ---- |
|     | *dptr = *eptr; | int digit_low = Hex_Values[*(++eptr)];     |      |
|     | }              | if (digit_high == -1 || digit_low == -1) { |      |
|     |                | False                                      | True |
= {“first+test%9Ktest%K9”}
T
H I
else { ok = 1;
4
*dptr = 16 * digit_high +  }
C = 7/8 = 87%
digit_low;
branch
}
C = 10/10 = 100%
bcond
| *dptr = '\0'; | M   | ++dptr; | L   |
| ------------- | --- | ------- | --- |
| return ok;    |     | ++eptr; |     |
| }             |     | }       |     |
24

Basic conditions vs branches
Basic condition coverage can be satisfied
without satisfying branch coverage
|        | “                    |     | ”   |     |
| ------ | -------------------- | --- | --- | --- |
| T4 = { | first+test%9Ktest%K9 |     | }   |     |
digit_high == -1  digit_low == -1 digit_high == -1 || digit_low == -1
|     | false | true  |     | true |
| --- | ----- | ----- | --- | ---- |
|     | true  | false |     | true |
Branch and basic condition are not comparable
neither implies the other
25

Covering branches and conditions
Branch and condition coverage:
Each decision and each basic condition must be true and
false at least once
= branch coverage and condition coverage
Compound condition coverage:
Each possible evaluation of each decision must be taken
at least once
digit_high == 1
All branches of the decision tree
false true
a.k.a. multiple condition coverage
digit_low == -1 TRUE
false true
FALSE TRUE
26

Compound conditions:
Exponential complexity
F = (((a || b) && c) || d) && e
a
| Test  | a  b  | c  d | e F  |     |     |     |     |     |     |
| ----- | ----- | ---- | ---- | --- | --- | --- | --- | --- | --- |
Case
|      |     |     |     |            | c    |            |       | b           |         |
| ---- | --- | --- | --- | ---------- | ---- | ---------- | ----- | ----------- | ------- |
| (1)  | T — | T — | T T |            |      |            |       |             |         |
| (2)  | T — | T — | F F |            |      |            |       |             |         |
| (3)  | T — | F T | T T |            |      |            |       |             |         |
| (4)  | T — | F T | F F | e          |      | d          | c     |             | d       |
| (5)  | T — | F F | — F |            |      |            |       |             |         |
| (6)  | F T | T — | T T |            |      |            |       |             |         |
| (7)  | F T | T — | F F |            |      |            |       |             |         |
|      |     |     |     | TRUE FALSE |      | e FALSE    | e     | d           | e FALSE |
| (8)  | F T | F T | T T |            |      |            |       |             |         |
| (9)  | F T | F T | F F |            |      |            |       |             |         |
| (10) | F T | F F | — F |            |      |            |       |             |         |
| (11) | F F | — T | T T |            | TRUE | FALSE TRUE | FALSE | eFALSE TRUE | FALSE   |
| (12) | F F | — T | F F |            |      |            |       |             |         |
| (13) | F F | — F | — F |            |      |            |       |             |         |
TRUE FALSE
| N conditions ⇒       |     | O(2N) test cases |     |     |     |     |     |     |     |
| -------------------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
| only && or only || ⇒ |     | N+1 test cases   |     |     |     |     |     |     |     |
27

Modified condition/decision (MC/DC)
Modified condition/decision (MC/DC) coverage:
Each basic condition is shown to independently
affect the decision
Motivation: test important combinations of
conditions, without exponential blowup
Requires, for each basic condition C in a decision D,
two test cases such that:
values of all evaluated conditions except C are the
same, and
D evaluates to true for one and false for the other
28

MC/DC: linear complexity
F = (((a || b) && c) || d) && e
| Test | a  b  | c  d | e  F |
| ---- | ----- | ---- | ---- |
Case
| (1)  | T -- | T -- | T T  |
| ---- | ---- | ---- | ---- |
| (2)  | T -- | T -- | F F  |
| (3)  | T -- | F T  | T T  |
| (5)  | T -- | F F  | -- F |
| (6)  | F T  | T -- | T T  |
| (13) | F F  | -- F | -- F |
Underlined values independently affect the output of the decision
| N basic conditions ⇒ |     | N+1 test cases |     |
| -------------------- | --- | -------------- | --- |
A good balance of thoroughness and test size  (and therefore widely used)
Required by safety standards for avionics software (DO-178B = ED-12B)
29

MC/DC vs. others
MC/DC is
compound condition
basic condition coverage (C)
decision (=branch) coverage (DC)
MC/DC
plus one additional condition (M):
every condition must
branch-condition
independently affect the
decision's output
branch basic condition
statement
30

Path coverage
Decision and condition coverage
consider individual program
decisions
Should we explore sequences of
decisions in the control flow?
= Paths
Many more paths than branches
31

Path Testing
Path coverage:
Each path must be executed at least once
# executed paths
Measure: C =
path # paths
Which paths?
32

Practical path coverage criteria
Program with loops ⇒ infinite number of paths
full path coverage is usually impossible to satisfy
# paths = ∞
Feasible criterion: Partition infinite set of paths
into a finite number of classes
By limiting
the number of traversals of loops
the length of the paths to be traversed
the dependencies among selected paths
33

Boundary interior path testing
Boundary interior path coverage:
Each path up to the first repeated node must be
executed at least once
Loops must be iterated zero times and at least one time
Group together paths that differ only in the subpath
they follow when repeating the body of a loop
Construction: unfold the CFG up to the first
repeated node
34

Boundary interior coverage: cgi-decode
| CFG | boundary/interior | paths |
| --- | ----------------- | ----- |
35

Limitations of boundary interior
coverage
The number of paths can still grow exponentially
N branches ⇒
if (a) {
S1;
2N boundary-interior paths
}
if (b) {
S2;
}
if (c) {
S3;
}
...
if (x) {
Sn;
}
36

Loop boundary testing
Loop boundary coverage:
Each loop body must be iterated zero times,
one time and more than one time at least once
Variant of the boundary/interior criterion
treats loop boundaries similarly
less stringent with respect to other differences
among paths
37

Linear Code Sequence and Jump
Example of Control Flow Graph
Linear Code Sequence and Jump (LCSJ)
Linear Code Sequence and Jump
public static String collapseNewlines(String argStr) Essentially subpaths of the control flow graph from one
public( sLtaCtiSc JS)tr:ing collapseNewlines(String argStr)
entry
branch to another
|     {    |                           |  {  |     |     |     |     |     |     |     |     |     |     |     |     |
| -------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Subpaths | from one branching point  |     |     |     | b2  |     |     |     |     |     |     |     |     |     |
        char last = argStr.charAt(0);         char last = argStr.charAt(0);
to another (jumps)         StringBuffer argBuf = new StringBuffer();
        StringBuffer argBuf = new StringBuffer();
        for (int cIdx = 0 ;  public static String collapseNewlines(String argStr) b1
proceeding to next block is not
        for (int cbIdrxa =n c0 h; cinIdgx < argStr.length(); cIdx++) From Sequence of basic blocs To
|           |     |     | cIdx < argStr.length(); | b3  |     |     |  {                                    |     |     | b2  |     |     |     |     |
| --------- | --- | --- | ----------------------- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|         { |     |     |                         |     |     |     |         char last = argStr.charAt(0); |     |     |     |     |     |     |     |
False True         StringBuffer argBuf = new StringBuffer(); Entry b1 b2 b3 jX
            char ch = argStr.charAt(cIdx);
| From | Sequence of basic blocs | To  |     |     |     |     |         for (int cIdx = 0 ;  |     |     |     |     |     |     |     |
| ---- | ----------------------- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- |
|      |                         |     | {   |     | b4  |     |                              |     |     |     |     |     |     |     |
            if (ch != '\n' || last != '\n')
jX             char ch = argStr.charAt(cIdx); Entry b1 b2 b3 b4 jT
            if (ch != '\n'
|          E   n{ try | b1 b2 b3 | jX  |     |     |     |     | cIdx < argStr.length(); |     | b3  |     |     |     |     |     |
| ------------------- | -------- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- |
                argBuf.append(ch); True False True Entry b1 b2 b3 b4 b5 jE
|           |               |     |     | False |     |     | jX  |     |     |     |     |     |     |     |
| --------- | ------------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E n t r y | b 1  b2 b3 b4 | jT  |     |       |     |     |     |     |     | b4  |     |     |     |     |
                   l a st =  ch ;  || last != '\n') b5 jT jL {
            char ch = argStr.charAt(cIdx); Entry b1 b2 b3 b4 b5 b6 b7 jL
            }
| Entry     | b1 b2 b3 b4 b5       | jE  |     | True                   |              |     |     |             if (ch != '\n'  |            |     |     |     |     |     |
| --------- | -------------------- | --- | --- | ---------------------- | ------------ | --- | --- | --------------------------- | ---------- | --- | --- | --- | --- | --- |
|         } |                      |     |     | {                      |              |     |     |                             | False True |     |     |     |     |     |
|           |                      |     | jE  |                        |              | b6  |     |                             |            |     | jX  | b8  |     | ret |
|           |                      |     |     |                 argBuf | .append(ch); |     |     |                             |            | jT  |     |     |     |     |
| Entry     | b1 b2 b3 b4 b5 b6 b7 | jL  |     |                        |              |     |     |  || last != '\n')           | b5         |     |     |     |     |     |
|           |                      |     |     |                 last   | = ch;        |     |     |                             |            |     |     |     |     |     |
            }
|         return argBuf.toString(); |     |     |     |       |     |     |     |     | True |     | jL  | b3 b4 |     | jT  |
| --------------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | ---- | --- | --- | ----- | --- | --- |
| jX                                | b8  | ret |     |       |     |     |     | jE  | {    |     |     |       |     |     |
|     }                             |     |     |     | False |     |     |     |     |      | b6  |     |       |     |     |
                argBuf.append(ch);
|     |       |     |     | }       |     | b7  |     |     |                 last  = ch; |     | jL  | b3 b4 b5 |     | jE  |
| --- | ----- | --- | --- | ------- | --- | --- | --- | --- | --------------------------- | --- | --- | -------- | --- | --- |
| jL  | b3 b4 | jT  |     |         |     |     |     |     |                             |     |     |          |     |     |
|     |       |     |     | cIdx++) |     |     |     |     |             }               |     |     |          |     |     |
False
|     |          |     |     |     |     |     |     |     |     |     | jL  | b3 b4 b5 b6 b7 |     | jL  |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- |
| jL  | b3 b4 b5 | jE  |     |     |     |     |     |     |     |     |     |                |     |     |
} b7
cIdx++)
|     |                |     | return argBuf.toString(); |     | b8  |     |     |     |     |     |     |     |     |     |
| --- | -------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| jL  | b3 b4 b5 b6 b7 | jL  |     }                     |     |     |     |     |     |     |     |     |     |     |     |
|     |                | ret |                           |     |     |     |     |     |     | jL  |     |     |     |     |
b8
return argBuf.toString();
38
    }
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 9 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 10
Interprocedural control flow graph Overestimating the calls relation
The static call graph includes calls through dynamic
| • Call graphs |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bindings that never occur in execution.
– Nodes represent procedures
public class C {
• Methods
    public static C cFactory(String kind) {
if (kind == "C") return new C();
• C functions
if (kind == "S") return new S();
return null;
• ...     }
    void foo() {
System.out.println("You called the parent's method");
– Edges represent calls relation
    }
    public static void main(String args[]) {
(new A()).check();
    } A.check()
}
class S extends C {
    void foo() {
System.out.println("You called the child's method");
    }
}
class A {
    void check() {
C myC = C.cFactory("S");
|     |     |     |     |     |     |     |     |     |     | C.foo() |     | S.foo() | CcFactory(string) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ----------------- | --- |
myC.foo();
    }
}
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 11 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 12

LCSAJ coverage
N-LCSAJ coverage:
Each sequence of N consecutive LCSAJ must be
executed at least once
1-LCSAJ is almost the same as branch coverage
TER (test effectiveness ratio) criteria:
TER = statement coverage
1
TER = branch coverage
2
TER = N-LCSAJ coverage
N+2
39

| Cyclomatic |     |     |     | analysis |     |     |     |     |
| ---------- | --- | --- | --- | -------- | --- | --- | --- | --- |
On a control flow graph
1
|     | Any path | p represented |     |     | as a vector |     | (v … v | )   |
| --- | -------- | ------------- | --- | --- | ----------- | --- | ------ | --- |
| 2   |          |               |     |     |             |     | 1      | n   |
3
|     | v = number |     | of times edge |     | i appears |     | in p |     |
| --- | ---------- | --- | ------------- | --- | --------- | --- | ---- | --- |
i
5
| 4   | e.g. p = A B C D F L B C E L B M = (1 1 2 1 1 1 0 0 0) |     |     |     |     |     |     |     |
| --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
7
6
|     | p is linearly |           | dependent |     | on p                  | , …, p |     |     |
| --- | ------------- | --------- | --------- | --- | --------------------- | ------ | --- | --- |
| 8 9 |               |           |           |     |                       | 1      | n   |     |
|     | iff p = k     | p         | + … + k   | p   |                       |        |     |     |
|     |               | 1 1       |           | n n |                       |        |     |     |
|     | e.g.          | p = A B M |           |     | = (1 1 0 0 0 0 0 0 0) |        |     |     |
1
|     |     | p = A B C E L B M |     |     | = (1 1 1 0 1 0 0 0 0) |     |     |     |
| --- | --- | ----------------- | --- | --- | --------------------- | --- | --- | --- |
2
|     |     | p = A B C D F L B M  |     |     | = (1 1 1 1 0 1 0 0 0) |     |     |     |
| --- | --- | -------------------- | --- | --- | --------------------- | --- | --- | --- |
3
|     |     | p = p | + p | – p |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- |
|     |     |       | 2 3 | 1   |     |     |     |     |
40

Cyclomatic complexity
|     | Basis set:  | a maximal set of linearly |             |             |     |          |           |
| --- | ----------- | ------------------------- | ----------- | ----------- | --- | -------- | --------- |
|     | independent |                           | paths       |             |     |          |           |
| 1   | Any         | path                      | is a linear | combination |     | of paths | from the  |
basis sets
2
| 3   | e.g. | p = A B M |     |     | = (1 1 0 0 0 0 0 0 0) |     |     |
| --- | ---- | --------- | --- | --- | --------------------- | --- | --- |
1
|     |     | p = A B C E L B M |     |     | = (1 1 1 0 1 0 0 0 0) |     |     |
| --- | --- | ----------------- | --- | --- | --------------------- | --- | --- |
2
5
|     |     | p = A B C D F L B M  |     |     | = (1 1 0 1 0 1 0 0 0) |     |     |
| --- | --- | -------------------- | --- | --- | --------------------- | --- | --- |
4
3
p = A B C D G H L B M= (1 1 0 1 0 0 1 1 0)
4
| 7   |     | p = A B C D G I L B M  |     |     | = (1 1 0 1 0 0 1 0 1) |     |     |
| --- | --- | ---------------------- | --- | --- | --------------------- | --- | --- |
6
5
| 8 9 | Cyclomatic        |               | number:    |                |     |     |     |
| --- | ----------------- | ------------- | ---------- | -------------- | --- | --- | --- |
|     | the number        |               | of paths   | in a basis set |     |     |     |
|     | v(CFG) = #edges – |               |            | #nodes + 2     |     |     |     |
|     | = # decision      |               | points + 1 |                |     |     |     |
|     | e.g.              | v(CFG) = 14 – |            | 11 + 2 = 5     |     |     |     |
41

Cyclomatic testing
Cyclomatic coverage:
A basis of independent paths must be executed at least
once
Number of cases is linear
v(CFG) = # edges - #nodes + 2
In practice:
• count the paths covered
• eliminate dependent paths
• stop when v(CFG) independent paths covered
42

Subsumption relation
Path Testing
Boundary interior testing Compound condition testing
Cyclomatic testing MC/DC testing
Branch and condition testing LCSAJ testing
Branch testing
Basic condition testing Loop boundary testing Statement testing
AIRETIRC
LACITEROEHT
AIRETIRC
LACITCARP
TER
3
TER
2
TER 1
43

Procedure calls
So far: intra-procedural coverage criteria
Ok for unit testing,
not well suited to integration or system testing
If unit testing has been effective,
then faults that remain to be found in integration
testing will be primarily interface faults
Testing effort should focus on interfaces between
units rather than their internal details
⇒ inter-procedural
44

Procedure call testing
Procedure A calls procedure B
What coverage criteria in A?
Entry/exit point coverage
B may have multiple entry points (e.g., Fortran)
and multiple exit points
Call coverage
B may be called from many points in A
Internal state, dynamic binding (objects)
Consider sequence of calls
45

DATA FLOW TESTING
46

|                        |                | Why               |             | Data Flow Testing? |           |                 |               |            |      |                |            |
| ---------------------- | -------------- | ----------------- | ----------- | ------------------ | --------- | --------------- | ------------- | ---------- | ---- | -------------- | ---------- |
| Statement, branch      |                |                   |             |                    | coverage  |                 | (node, edge): |            |      |                |            |
|                        | Don’t          | test interactions |             |                    |           |                 |               |            |      |                |            |
| Path-based             |                |                   | coverage:   |                    |           |                 |               |            |      |                |            |
|                        | Require        |                   | impractical |                    |           | number          | of test cases |            |      |                |            |
|                        | And only       |                   | a few       | paths              |           | uncover         |               | additional |      | faults, anyway |            |
| Need                   |                | to distinguish    |             |                    | important |                 |               | paths      |      |                |            |
| Intuition:  statements |                |                   |             |                    |           | interact        |               | through    |      | data flow      |            |
|                        | Value computed |                   |             |                    | in one    | statement, used |               |            |      | in another     |            |
|                        | Bad            | value             | computation |                    |           | revealed        |               | only       | when |                | it is used |
47

Data flow concept
x defined in 1 and 4
1
x used in 6
x = ....
Value of x at 6 could be
2
if .... computed at 1 or at 4
(1,6) and (4,6) are
3
4
.... x = ....
def-use (DU) pairs
5
...
Bad computation at 1 or 4
6
could be revealed only if they
y = x + ...
are used at 6
⇒ test paths from 1 and 4 to 6
48

Terms
| DU pair: a pair             |                    | of definition |                          | and use  |                    | for some  |         |
| --------------------------- | ------------------ | ------------- | ------------------------ | -------- | ------------------ | --------- | ------- |
| variable, such              |                    | that          | at least                 | one      | DU path            | exists    | from    |
| the definition              |                    | to the use    |                          |          |                    |           |         |
| DU path: a definition-clear |                    |               |                          | path     | on the CFG from a  |           |         |
| definition                  | to a use of a same |               |                          | variable |                    |           |         |
| Note –                      | loops              | could         | create infinite DU paths |          |                    |           |         |
| Definition-clear:  variable |                    |               |                          | is not   | redefined          |           | on path |
49

Definition-clear path
1,2,3,5,6 is a definition-clear
1 path from 1 to 6
x = ....
x is not re-assigned between 1
2 and 6
if ....
1,2,4,5,6 is not a definition-
3
4 clear path from 1 to 6
.... x = ....
the value of x is “killed”
5
(reassigned) at node 4
...
(1,6) is a DU pair because
6
y = x + ... 1,2,3,5,6 is a definition-clear
path
50

Data-flow Coverage criteria
All DU pairs:
| Each | DU pair |     | is exercised |     | at least |     | once |     |
| ---- | ------- | --- | ------------ | --- | -------- | --- | ---- | --- |
All DU paths:
| Each | simple |     | (non looping) DU path |     |     |     | is exercised | at least |
| ---- | ------ | --- | --------------------- | --- | --- | --- | ------------ | -------- |
once
| often |     | impractical |     |     |     |     |     |     |
| ----- | --- | ----------- | --- | --- | --- | --- | --- | --- |
All definitions:
| For each |     | definition, some DU pair |     |     |     |     | is exercised | at least |
| -------- | --- | ------------------------ | --- | --- | --- | --- | ------------ | -------- |
once
| (Every |     | computed |     | value | is used | somewhere) |     |     |
| ------ | --- | -------- | --- | ----- | ------- | ---------- | --- | --- |
51

Difficult cases
Arrays:
x[i] = a ; ... ; y = x[j] ;
DU pair (only) if i==j
Pointers:
p = &x ; ... ; *p = 99 ; ... ; q = x ;
*p is an alias of x
Objects:
m.putFoo(...); ... ; y=n.getFoo(...);
Are m and n the same object?
Do m and n share a “foo” field?
Aliases:
Which references are (always or sometimes) the same?
52

Data flow coverage with complex
structures
| Arrays and pointers |                  |     | are critical |     |     | for data flow analysis |                      |        |     |       |
| ------------------- | ---------------- | --- | ------------ | --- | --- | ---------------------- | -------------------- | ------ | --- | ----- |
|                     | Under-estimation |     | of aliases   |     | ⇒   | some DU pairs          |                      | missed |     |       |
|                     | Over-estimation  |     | of aliases   |     | ⇒   | may                    | introduce unfeasible |        |     | test  |
obligations
| For testing, it |                              | may | be preferable |              |     | to accept  |                       | under-estimation |          |     |
| --------------- | ---------------------------- | --- | ------------- | ------------ | --- | ---------- | --------------------- | ---------------- | -------- | --- |
|                 | Controversial: In other      |     |               | applications |     |            | (e.g., compilers), a  |                  |          |     |
|                 | conservative over-estimation |     |               |              |     | of aliases | is usually            |                  | required |     |
May rely on external guidance or other global analysis to calculate
good estimates
Undisciplined use of dynamic storage, pointer arithmetic, etc.
|     | may make | the whole |     | analysis | infeasible |     |     |     |     |     |
| --- | -------- | --------- | --- | -------- | ---------- | --- | --- | --- | --- | --- |
53

Unfeasible criteria
Sometimes criteria may not be satisfiable
Even in well-designed, well-maintained systems
Statements that cannot be executed
defensive programming
code reuse (parts not used)
Conditions that cannot be satisfied
interdependent conditions
paths that cannot be executed
interdependent decisions
54

Unfeasible data flow
Data-flow criteria = paths
1
if (cond)
F
T
Suppose cond has not changed
| 2 3   |           |     |
| ----- | --------- | --- |
| ....  | x = ....  |     |
between 1 and 5
Or different conditions,
4
...
first implies second
5
if (cond)
| T            | F     | (3, 6) is not a feasible DU pair |
| ------------ | ----- | -------------------------------- |
| 6 7          |       |                                  |
| y = x + ...  | ....  | No test case can cover it        |
55

Unfeasible criteria
Difficult or impossible to determine
| Impossible to decide feasible |         | paths      |          |
| ----------------------------- | ------- | ---------- | -------- |
| Solutions:                    | achieve | reasonable | coverage |
set a coverage goal less than 100%
require justification of elements left uncovered
RTCA-DO-178B and EUROCAE ED-12B for modified
MC/DC
56

Summary
We defined a number of coverage criteria
NOT test design techniques!
Different criteria address different classes of errors
Full coverage is usually unattainable
Remember that attainability is an undecidable problem!
“ ”
…and when attainable, inversion is usually hard
Find program inputs achieving a covering objective
Automated support exist
Rather than requiring full coverage,
measure the degree of coverage
May drive test improvement
57

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 12, 13
58

Software Quality Assurance
5 – More Testing
Charles Pecheur
Mar 2018
1

More Testing
Model-based testing
State machines
Decision structures
Grammars
Testing object-oriented software
State models
Polymorphism, inheritance, genericity
Fault-based testing
Mutation testing
Fault estimation
2

MODEL-BASED TESTING
3

Functional vs structural test: granularity
Steps: From specification to test cases
levels
• Functional test applies at all granularity levels: • 1. Decompose the specification
– Unit (from module interface spec) – If the specification is large, break it into independently
testable features to be considered in testing
– Integration (from API or subsystem spec)
• 2. Select representatives
– System (from system requirements spec)
– Representative values of each input, or
– Regression (from system requirements + bug history)
– Representative behaviors of a model
• Structural (code-based) test design applies to
– Often simple input/output transformations don’t describe a
relatively small parts of a system: system. We use models in program specification, in program
design, and in test design
– Unit
• 3. Form test specifications
– Integration
– Typically: combinations of input values, or model behaviors
• 4. Produce and execute actual tests
(c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 13 (c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 14
Structured specifications
From specification to test cases Simple example: Postal code lookup
Functional testing
Based on requirements,
specifications
Combinatorial testing
Test combinations of orthogonal
• Input: ZIP code (5-digit
choices US Postal code)
• Output: List of cities
category-partition
• What are some
representative values (or
classes of value) to test?
There are structured specifications
State machines, tables, graphs,
(c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 15 (c) 2007 Mauro Pezzè & Michal Young Ch 10, slide 16
grammars, …
What tests for those
specifications?
4

|                        | Contex Insensitive Call graphs |     |     |     |     |                        | Contex Sensitive Call graphs |     |     |     |     |     |     |     |
| ---------------------- | ------------------------------ | --- | --- | --- | --- | ---------------------- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- |
| public class Context { |                                |     |     |     |     | public class Context { |                              |     |     |     |     |     |     |     |
    public static void main(String args[]) {     public static void main(String args[]) {
| Context c = new Context(); |     |     |     |      |     | Context c = new Context(); |     |     |     |      |     |     |     |     |
| -------------------------- | --- | --- | --- | ---- | --- | -------------------------- | --- | --- | --- | ---- | --- | --- | --- | --- |
| c.foo(3);                  |     |     |     | main |     | c.foo(3);                  |     |     |     | main |     |     |     |     |
| c.bar(17);                 |     |     |     |      |     | c.bar(17);                 |     |     |     |      |     |     |     |     |
|     }                      |     |     |     |      |     |     }                      |     |     |     |      |     |     |     |     |
|     void foo(int n) {      |     |     |     |      |     |     void foo(int n) {      |     |     |     |      |     |     |     |     |
int[]  myArray = new int[ n ]; int[]  myArray = new int[ n ];
| depends( myArray, 2) ; |     |     |       |       |     | depends( myArray, 2) ; |     |     |     |     |           |     |     |     |
| ---------------------- | --- | --- | ----- | ----- | --- | ---------------------- | --- | --- | --- | --- | --------- | --- | --- | --- |
|     }                  |     |     | C.foo | C.bar |     |     }                  |     |     |     |     | C.bar(17) |     |     |     |
C.foo(3)
Model-based testing
|     void bar(int n) { |     |     |     |     |     |     void bar(int n) { |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
int[]  myArray = new int[ n ]; int[]  myArray = new int[ n ];
| depends( myArray, 16) ; |     |     |     |           |     | depends( myArray, 16) ; |     |                       |     |                        |     |     |     |     |
| ----------------------- | --- | --- | --- | --------- | --- | ----------------------- | --- | --------------------- | --- | ---------------------- | --- | --- | --- | --- |
|     }                   |     |     |     |           |     |     }                   |     |                       |     |                        |     |     |     |     |
|                         |     |     |     | C.depends |     |                         |     | C.depends(int!3),a,2) |     | C.depends (int!3),a,2) |     |     |     |     |
    void depends( int[] a, int n ) {     void depends( int[] a, int n ) {
| a[n] = 42; |     |     |     |     |     | a[n] = 42; |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     }      |     |     |     |     |     |     }      |     |     |     |     |     |     |     |     |
Principle:
| }   |     |     |     |     |     | }   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Devise test cases to check actual behavior against
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 13 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 14
behavior specified by the model
Context Sensitive CFG
|     |     |     |     |     | Coverage |     | similar to |     | structural testing,  |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | --- | ---------- | --- | -------------------- | --- | --- | --- | --- | --- |
Finite state machines
exponential growth
|     |     |     |     |     | but applied to specification |                                           |     |     |     |     | and design models |     |     |     |
| --- | --- | --- | --- | --- | ---------------------------- | ----------------------------------------- | --- | --- | --- | --- | ----------------- | --- | --- | --- |
|     |     |     |     |     |                              | • finite set of states (nodes)            |     |     |     |     |                   |     |     |     |
|     | A   |     |     |     |                              | • set of transitions among states (edges) |     |     |     |     |                   |     |     |     |
1 context A Graph representation (Mealy machine) Tabular representation
|     | B   | C   |     |     |     |        |     |            |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |    LF_ |     | Other char |     |     |     |     |     |     |
|     |     |     |     |     |     | emit   |     | apend      |     |     |     |     |     |     |
   LF_
2 contexts AB AC
emit
|     | D   |                            |     |     |     |        |            |        | LF       | CR     | EOF | other    |     |     |
| --- | --- | -------------------------- | --- | --- | --- | ------ | ---------- | ------ | -------- | ------ | --- | -------- | --- | --- |
|     |     | E                          |     |     |     | e      |            | w      |          |        |     |          |     |     |
|     |     |                            |     |     |     | Emty   |            | Within |          |        |     |          |     |     |
|     |     |                            |     |     |     | buffer |            | line   |          |        |     |          |     |     |
|     |     |                            |     |     |     |        | Other char |        | e e/emit | e/emit | d/- | w/append |     |     |
|     |     | 4 contexts ABD ABE ACD ACE |     |     |     |        | append     |        |          |        |     |          |     |     |
F
|     |     | G   |     |     |     |     |     |     | w e/emit | e/emit | d/emit | w/append |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ------ | -------- | --- | --- |
Other char
|     |     |     |     |     |     |   CR_  | append |  EOF |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | ------ | ---- | --- | --- | --- | --- | --- | --- |
LF
|     |     |              |     |     |     | emit |        | emit |       | LF, LF | ,  a, CR | ,   E O F     |      | ?   |
| --- | --- | ------------ | --- | --- | --- | ---- | ------ | ---- | ----- | ------ | -------- | ------------- | ---- | --- |
|     |     |              |     |     |     |      |   CR_  |      | l e/- |        | d /-     | w/ a p p en d | P(x) |     |
|     |     | 8 contexts … |     |     |     |      | emit   |      |       |        |          |               |      |     |
|     | H   | I            |     |     |     |      |        |      |       |        |          |               |      |     |
|     |     |              |     |     |     | l    |        | d    |       |        |          |               |      |     |
Looking for
|     |     |                       |     |     |     | optional DOS LF |     | Done |     |     |     |     |     |     |
| --- | --- | --------------------- | --- | --- | --- | --------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
|     |     | 16 calling contexts … |     |     |     |                 | EOF |      |     |     |     |     |     |     |
EOF 5
J
(c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 15 (c) 2007 Mauro Pezzè & Michal Young  Ch 5, slide 16

From an informal specification…
Maintenance: The Maintenance function records the history of items undergoing
maintenance.
If the product is covered by warranty or maintenance contract, maintenance can be
Multiple choices in the first step
requested either by calling the maintenance  toll free number, or through the web site, or
|     |     |     |     |     |     |     |     |     | by bringing the item to a designated maintenance station. |     |     |     |     | ... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
If the maintenance is requested by phone or web site and the customer is a US or EU
resident, the item is picked up at the customer site, otherwise, the customer shall ship the
Deriving test cases from finite state
item with an express courier.
If the maintenance contract number provided by t.h..e  dceustteormmeirn ies  nthote v paloids,s tihbei liittieems follows
machines
the procedure for items not covered by warranty.
for the next step ...
If the product is not covered by warranty or maintenance contract, maintenance can be
requested only by bringing the item to a maintenance station. The maintenance station
informs the customer of the estimated costs for repair. Maintenance starts only when the
customer accepts the estimate.
A common kind of model for
|     |     |     |     |     |     |     |     |     | If the customer does not accept the estimate, the product is returned to the customer. |     |     |     | ... and so on ... |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------------------------------- | --- | --- | --- | ----------------- | --- | --- |
Small problems can be repaired directly at the maintenance station. If the maintenance
describing behavior that depends on
station cannot solve the problem, the product is sent to the maintenance regional
headquarters (if in US or EU) or to the maintenance main headquarters (otherwise).
sequences of events or stimuli
If the maintenance regional headquarters cannot solve the problem, the product is sent to
the maintenance main headquarters.
Example: UML state diagrams Maintenance is suspended if some components are not available.
Once repaired, the product is returned to the customer.
Finite state machines
(c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 5 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 6
0
| For describing dynamic  |     |     |     |     | NO  |     |     |     |     |     |     |     |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Maintenance
…to a test suite
|                           |     |     |         | t                  |                                           | b r e q            |                     |       |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | ------- | ------------------ | ----------------------------------------- | ------------------ | ------------------- | ----- | --- | --- | --- | --- | --- | --- | --- |
| behavior that depends on  |     |     | pick up | s t  a ion         |                                           | y   p u e          |                     |       |     |     |     |     |     |     |     |
|                           |     |     |         | q u e s ta t       | [ U                                       | S h o n s t        | return …to a finite |       |     |     |     |     |     |     |     |
|                           |     |     |         | r e n c e   )      | reiruoc sserpxe yb ro (                   |   o r e   o        |                     |       |     |     |     |     |     |     |     |
|                           |     |     |         | n a n ty           | noitats ecnanetniam )rebmun tcartnoc( c o | n E U r   w        |                     |       |     |     |     |     |     |     |     |
|                           |     |     |         | main t e w a r r a |                                           | t ra   r e s e b   |                     |       |     |     |     |     |     |     |     |
|                           |     |     |         | o                  |                                           | c t   n i d e      |                     |       |     |     |     |     |     |     |     |
|                           |     |     |         | (n                 |  ta tseuqer                               | u m n t]           |                     |       |     |     |     |     |     |     |     |
| sequences of events       | or  |     |         |                    |                                           | b e                |                     | state |     |     |     |     |     |     |     |
|                           |     | 1   |         |                    |                                           | r )                |                     |       |     |     |     |     |     |     |     |
2
|     |     | Wait for  |     Maintenance |     |     | 3   |     |     |     |     |     |     |     |     |     |
| --- | --- | --------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Wait for
returning (no warranty) pick up Meaning: From state 0 to state
machine…
| stimuli |     |          |          | in       |     |         |     |     |     |     |     |     |                                    |     |     |
| ------- | --- | -------- | -------- | -------- | --- | ------- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- |
|         |     |          | etamitse | c on v a |     |         |     |     |     |     |     |     | 2 to state 4 to state 1 to state 0 |     |     |
|         |     | reje     | stsoc    | l id     |     |         |     |     |     |     |     |     |                                    |     |     |
|         |     |          |          | nu t r a |     |         |     |     | TC1 | 0 2 | 4 1 | 0   |                                    |     |     |
|         |     | ct estim |          | m c t    |     | pick up |     |     |     |     |     |     |                                    |     |     |
b e
r
ate
Example: UML state
|     |     |     | 4          |          | 5 Repair      |                  | 6        |     |     |     |     |     |     |     |     |
| --- | --- | --- | ---------- | -------- | ------------- | ---------------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | Wait for   | accept   |               |                  |          |     |     |     |     |     |     |     |     |
|     |     |     |            |          | (maintenance  | repair completed | Repaired |     | TC2 | 0 5 | 2 4 | 5 6 | 0   |     |     |
|     |     |     | acceptance | estimate |               |                  |          |     |     |     |     |     |     |     |     |
station)
diagrams (hierarchic)
|     |     |     |     | mponent (a) | (Uun     |                   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ----------- | -------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |             | S a b    | successful repair |     |     |     |     |     |     |     |     |     |
|     |     |     |     |             |  or E le |                   |     |     | TC3 | 0 3 | 5 9 | 6 0 |     |     |     |
  t
U o   re
|     |     |     |     | lack co |   r                |         |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | ------------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |         | c o m p o n e n t  | e s p a |     |     |     |     |     |     |     |     |     |
|     |     |     |     |         |                    | i d ir  |     |     |     |     |     |     |     |     |     |
|     |     |     |     |         | a r riv e s   (a ) | en      |     |     |     |     |     |     |     |     |     |
|     |     |     |     |         |                    | t )     | air |     |     |     |     |     |     |     |     |
ep
|     |     |     |           |                    |     |            | ul r |     | TC4 | 0 3 | 5 7 | 5 8 | 7   | 8 9 6 | 0   |
| --- | --- | --- | --------- | ------------------ | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | ----- | --- |
|     |     |     | 7         |                    |     | 8 Repair   | ssf  |     |     |     |     |     |     |       |     |
|     |     |     | Wait for  | lack component (b) |     | (regional  |      |     |     |     |     |     |     |       |     |
e
|     |     |     | component |     |     |               | cc  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |           |     |     | headquarters) | su  |     |     |     |     |     |     |     |     |
component
unable to
|     |     |         |                      | la arrives (b) |     | repair |     |     |     |     |     |             |                  |                     |     |
| --- | --- | ------- | -------------------- | -------------- | --- | ------ | --- | --- | --- | --- | --- | ----------- | ---------------- | ------------------- | --- |
|     |     |         |                      | c              |     |        |     |     |     |     |     | I s  t hi s |   a  t h o r o u | g h  t e st suite?  |     |
|     |     | u n a b | le   to  r e p a i r | k  c           |     |        |     |     |     |     |     |             |                  |                     |     |
o m
(not  U S   o r  E U   r e si d ent) ponent (c) H o w   c a n   w e   ju d g e ?
c o m p o n e n t
a r ri v e s   ( c )
9 Repair
(main
(c) 2007 Mauro Pezzè & Michal Young headquarters)  Ch 14, slide 7 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 8
6

Example : specification
Maintenance: The Maintenance function records the Multiple choices
history of items undergoing maintenance.
If the product is covered by warranty or maintenance
contract, maintenance can be requested either by calling
the maintenance toll free number, or through the web
Next step
site, or by bringing the item to a designated maintenance
station.
If the maintenance is requested by phone or web site
and the customer is a US or EU resident, the item is
picked up at the customer site, otherwise, the customer
shall ship the item with an express courier.
If the maintenance contract number provided by the
customer is not valid, the item follows the procedure for
etc …
items not covered by warranty.
If the product is not covered by warranty or
maintenance contract, maintenance can be requested
only by bringing the item to a maintenance station. The
maintenance station informs the customer of the
7
estimated costs for repair. Maintenance starts only when
the customer accepts the estimate.

From an informal specification…
Maintenance: The Maintenance function records the history of items undergoing
maintenance.
If the product is covered by warranty or maintenance contract, maintenance can be
Multiple choices in the first step
requested either by calling the maintenance  toll free number, or through the web site, or
|     |     |     |     |     |     |     |     | by bringing the item to a designated maintenance station. |     |     |     |     | ... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
If the maintenance is requested by phone or web site and the customer is a US or EU
resident, the item is picked up at the customer site, otherwise, the customer shall ship the
Deriving test cases from finite state
item with an express courier.
If the maintenance contract number provided by t.h..e  dceustteormmeirn ies  nthote v paloids,s tihbei liittieems follows
machines
the procedure for items not covered by warranty.
for the next step ...
If the product is not covered by warranty or maintenance contract, maintenance can be
requested only by bringing the item to a maintenance station. The maintenance station
informs the customer of the estimated costs for repair. Maintenance starts only when the
customer accepts the estimate.
A common kind of model for
|     |     |     |     |     |     |     |     | If the customer does not accept the estimate, the product is returned to the customer. |     |     |     | ... and so on ... |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------------------------------- | --- | --- | --- | ----------------- | --- | --- |
Small problems can be repaired directly at the maintenance station. If the maintenance
describing behavior that depends on
station cannot solve the problem, the product is sent to the maintenance regional
headquarters (if in US or EU) or to the maintenance main headquarters (otherwise).
sequences of events or stimuli
If the maintenance regional headquarters cannot solve the problem, the product is sent to
the maintenance main headquarters.
Example: UML state diagrams Maintenance is suspended if some components are not available.
Once repaired, the product is returned to the customer.
Example: state machine
(c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 5 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 6
0
NO
Maintenance
…to a test suite
|     |         |     |                | t           | b                                           | r e q         |                     |     |     |     |     |     |     |     |
| --- | ------- | --- | -------------- | ----------- | ------------------------------------------- | ------------- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
|     | pick up |     | s t  a         | ion         | y   p                                       | u e           |                     |     |     |     |     |     |     |     |
|     |         |     | q u e          | s ta t      | [ U S                                       | h o n s t     | return …to a finite |     |     |     |     |     |     |     |
|     |         |     | r e n c e      |   )         | reiruoc sserpxe yb ro (   o r               | e   o         |                     |     |     |     |     |     |     |     |
|     |         |     | n a            | n ty        | noitats ecnanetniam )rebmun tcartnoc( c o n | E U r   w     |                     |     |     |     |     |     |     |     |
|     |         |     | main t e w a r | r a         | t ra                                        |   r e s e b   |                     |     |     |     |     |     |     |     |
|     |         |     | o              |             | c                                           | t   n i d e   |                     |     |     |     |     |     |     |     |
|     |         |     | (n             |  ta tseuqer |                                             | u m n t]      |                     |     |     |     |     |     |     |     |
|     |         |     |                |             |                                             | b e           | state               |     |     |     |     |     |     |     |
| 1   |         |     |                |             |                                             | r )           |                     |     |     |     |     |     |     |     |
2
| Wait for  |     Maintenance |     |     |     |     | 3   |     |     |     |     |     |     |     |     |
| --------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Wait for
returning (no warranty) pick up Meaning: From state 0 to state
machine…
in
|          |     | etamitse | c on | v a   |     |         |     |     |     |     |     | 2 to state 4 to state 1 to state 0 |     |     |
| -------- | --- | -------- | ---- | ----- | --- | ------- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- |
| reje     |     | stsoc    |      | l id  |     |         |     |     |     |     |     |                                    |     |     |
|          |     |          | nu   | t r a |     |         |     | TC1 | 0 2 | 4 1 | 0   |                                    |     |     |
| ct estim |     |          | m    | c t   |     | pick up |     |     |     |     |     |                                    |     |     |
b e
r
ate
|     | 4          |           |          | 5 Repair      |     |                  | 6        |     |     |     |     |     |     |     |
| --- | ---------- | --------- | -------- | ------------- | --- | ---------------- | -------- | --- | --- | --- | --- | --- | --- | --- |
|     |            | Wait for  | accept   |               |     |                  |          |     |     |     |     |     |     |     |
|     |            |           |          | (maintenance  |     | repair completed | Repaired | TC2 | 0 5 | 2 4 | 5 6 | 0   |     |     |
|     | acceptance |           | estimate |               |     |                  |          |     |     |     |     |     |     |     |
station)
|     |     |     |     | mponent (a) | (Uun     |                   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ----------- | -------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |             | S a b    | successful repair |     |     |     |     |     |     |     |     |
|     |     |     |     |             |  or E le |                   |     | TC3 | 0 3 | 5 9 | 6 0 |     |     |     |
  t
U o   re
|     |     |     | lack co |               |   r         |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------- | ------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |         | c o m p o n e | n t e s p a |     |     |     |     |     |     |     |     |     |
i d ir
|     |     |     |     | a r riv e s   | (a ) en |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |               | t       | )   | air |     |     |     |     |     |     |     |
ep
|     |     |           |     |                    |     |            | ul r | TC4 | 0 3 | 5 7 | 5 8 | 7   | 8 9 6 | 0   |
| --- | --- | --------- | --- | ------------------ | --- | ---------- | ---- | --- | --- | --- | --- | --- | ----- | --- |
|     |     | 7         |     |                    | 8   | Repair     | ssf  |     |     |     |     |     |       |     |
|     |     | Wait for  |     | lack component (b) |     | (regional  |      |     |     |     |     |     |       |     |
e
|     |     | component |     |     |               |     | cc  |     |     |     |     |     |     |     |
| --- | --- | --------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |           |     |     | headquarters) |     | su  |     |     |     |     |     |     |     |
component
unable to
|         |                      |     | la  | arrives (b) |     | repair |     |     |     |     |             |                  |                     |     |
| ------- | -------------------- | --- | --- | ----------- | --- | ------ | --- | --- | --- | --- | ----------- | ---------------- | ------------------- | --- |
|         |                      |     | c   |             |     |        |     |     |     |     | I s  t hi s |   a  t h o r o u | g h  t e st suite?  |     |
| u n a b | le   to  r e p a i r |     | k   |  c          |     |        |     |     |     |     |             |                  |                     |     |
o m
(not  U S   o r  E U   r e si d ent) ponent (c) H o w   c a n   w e   ju d g e ?
|     |     |     | c o m p o    | n e n t |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | a r ri v e s |   ( c ) |     |     |     |     |     |     |     |     |     |     |
9 Repair
(main
(c) 2007 Mauro Pezzè & Michal Young headquarters)  Ch 14, slide 7 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 8
8

From an informal specification…
Maintenance: The Maintenance function records the history of items undergoing
maintenance.
If the product is covered by warranty or maintenance contract, maintenance can be
Multiple choices in the first step
requested either by calling the maintenance  toll free number, or through the web site, or
|     |     |     |     |     |     |     |     |     |     |     | by bringing the item to a designated maintenance station. |     |     |     |     | ... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
If the maintenance is requested by phone or web site and the customer is a US or EU
resident, the item is picked up at the customer site, otherwise, the customer shall ship the
Deriving test cases from finite state
item with an express courier.
If the maintenance contract number provided by t.h..e  dceustteormmeirn ies  nthote v paloids,s tihbei liittieems follows
machines
the procedure for items not covered by warranty.
for the next step ...
If the product is not covered by warranty or maintenance contract, maintenance can be
requested only by bringing the item to a maintenance station. The maintenance station
informs the customer of the estimated costs for repair. Maintenance starts only when the
customer accepts the estimate.
A common kind of model for
|     |     |     |     |     |     |     |     |     |     |     | If the customer does not accept the estimate, the product is returned to the customer. |     |     |     | ... and so on ... |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------------------------------- | --- | --- | --- | ----------------- | --- | --- |
Small problems can be repaired directly at the maintenance station. If the maintenance
describing behavior that depends on
station cannot solve the problem, the product is sent to the maintenance regional
headquarters (if in US or EU) or to the maintenance main headquarters (otherwise).
sequences of events or stimuli
If the maintenance regional headquarters cannot solve the problem, the product is sent to
the maintenance main headquarters.
Example: UML state diagrams Maintenance is suspended if some components are not available.
Once repaired, the product is returned to the customer.
Example: test suite
(c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 5 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 6
0
NO
Maintenance
…to a test suite
|     |     |     |     |     |     |         | t            |     | b r e q       |                     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | ------------- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | pick up | s t  a       | ion | y   p u e     |                     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |         | q u e s ta t | [ U | S h o n s t   | return …to a finite |     |     |     |     |     |     |     |
TC1 0 2 4 1 0 r e n c e   ) reiruoc sserpxe yb ro (   o r e   o
|     |     |     |     |     |     |     | n a n ty           | noitats ecnanetniam )rebmun tcartnoc( c o | n E U r   w        |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | ----------------------------------------- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | main t e w a r r a |                                           | t ra   r e s e b   |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     | o                  |                                           | c t   n i d e      |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     | (n                 |  ta tseuqer                               | u m n t]           |     |     |     |     |     |     |     |     |
b e state
|     |     |     |     |     | 1   |     |     |     | r ) |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
|     |       |       |     |     | Wait for  |     Maintenance |     |     | 3   |          |     |     |     |     |     |     |     |
| --- | ----- | ----- | --- | --- | --------- | --------------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
| TC2 | 0 5 2 | 4 5 6 | 0   |     |           |                 |     |     |     | Wait for |     |     |     |     |     |     |     |
returning (no warranty) pick up Meaning: From state 0 to state
machine…
in
|     |       |       |     |     |          | etamitse | c on v a |     |         |     |     |     |     |     | 2 to state 4 to state 1 to state 0 |     |     |
| --- | ----- | ----- | --- | --- | -------- | -------- | -------- | --- | ------- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- |
|     |       |       |     |     | reje     | stsoc    | l id     |     |         |     |     |     |     |     |                                    |     |     |
|     |       |       |     |     |          |          | nu t r a |     |         |     | TC1 | 0 2 | 4 1 | 0   |                                    |     |     |
|     |       |       |     |     | ct estim |          | m c t    |     | pick up |     |     |     |     |     |                                    |     |     |
| TC3 | 0 3 5 | 9 6 0 |     |     |          |          | b e      |     |         |     |     |     |     |     |                                    |     |     |
r
ate
|     |       |       |       |     |     | 4          |             | 5 Repair      |                  | 6                 |     |     |     |     |     |     |     |
| --- | ----- | ----- | ----- | --- | --- | ---------- | ----------- | ------------- | ---------------- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
|     |       |       |       |     |     | Wait for   | accept      |               |                  |                   |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            |             | (maintenance  | repair completed | Repaired          | TC2 | 0 5 | 2 4 | 5 6 | 0   |     |     |
|     |       |       |       |     |     | acceptance | estimate    |               |                  |                   |     |     |     |     |     |     |     |
| TC4 | 0 3 5 | 7 5 8 | 7 8 9 | 6 0 |     |            |             | station)      |                  |                   |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            | mponent (a) | (Uun          |                  |                   |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            |             | S a b         |                  | successful repair |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            |             |  or E le      |                  |                   | TC3 | 0 3 | 5 9 | 6 0 |     |     |     |
  t
|     |     |     |     |     |     |     |         | U                  | o   re  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | lack co |   r                |         |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         | c o m p o n e n t  | e s p a |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         |                    | i d ir  |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         | a r riv e s   (a ) | en      |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         |                    | t )     | air |     |     |     |     |     |     |     |
ep
|     |     |     |     |     |     |           |                    |     |            | ul r | TC4 | 0 3 | 5 7 | 5 8 | 7   | 8 9 6 | 0   |
| --- | --- | --- | --- | --- | --- | --------- | ------------------ | --- | ---------- | ---- | --- | --- | --- | --- | --- | ----- | --- |
|     |     |     |     |     |     | 7         |                    |     | 8 Repair   | ssf  |     |     |     |     |     |       |     |
|     |     |     |     |     |     | Wait for  | lack component (b) |     | (regional  |      |     |     |     |     |     |       |     |
e
| Is this | thorough? |     |     |     |     | component |     |     |               | cc  |     |     |     |     |     |     |     |
| ------- | --------- | --- | --- | --- | --- | --------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|         |           |     |     |     |     |           |     |     | headquarters) | su  |     |     |     |     |     |     |     |
component
unable to
|     |     |     |     |     |         |                      | la arrives (b) |     | repair |     |     |     |     |             |                  |                     |     |
| --- | --- | --- | --- | --- | ------- | -------------------- | -------------- | --- | ------ | --- | --- | --- | --- | ----------- | ---------------- | ------------------- | --- |
|     |     |     |     |     |         |                      | c              |     |        |     |     |     |     | I s  t hi s |   a  t h o r o u | g h  t e st suite?  |     |
|     |     |     |     |     | u n a b | le   to  r e p a i r | k  c           |     |        |     |     |     |     |             |                  |                     |     |
o m
How can we judge? (not  U S   o r  E U   r e si d ent) ponent (c) H o w   c a n   w e   ju d g e ?
c o m p o n e n t
a r ri v e s   ( c )
9 Repair
(main
(c) 2007 Mauro Pezzè & Michal Young headquarters)  Ch 14, slide 7 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 8
9

Covering finite state machines
State coverage:
Every state in the model should be visited at
least once
Transition coverage:
Every transition in the model should be
traversed at least once
This is the most commonly used criterion
10

From an informal specification…
Maintenance: The Maintenance function records the history of items undergoing
maintenance.
If the product is covered by warranty or maintenance contract, maintenance can be
Multiple choices in the first step
requested either by calling the maintenance  toll free number, or through the web site, or
|     |     |     |     |     |     |     |     |     |     |     | by bringing the item to a designated maintenance station. |     |     |     |     | ... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
If the maintenance is requested by phone or web site and the customer is a US or EU
resident, the item is picked up at the customer site, otherwise, the customer shall ship the
Deriving test cases from finite state
item with an express courier.
If the maintenance contract number provided by t.h..e  dceustteormmeirn ies  nthote v paloids,s tihbei liittieems follows
machines
the procedure for items not covered by warranty.
for the next step ...
If the product is not covered by warranty or maintenance contract, maintenance can be
requested only by bringing the item to a maintenance station. The maintenance station
informs the customer of the estimated costs for repair. Maintenance starts only when the
customer accepts the estimate.
A common kind of model for
|     |     |     |     |     |     |     |     |     |     |     | If the customer does not accept the estimate, the product is returned to the customer. |     |     |     | ... and so on ... |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------------------------------- | --- | --- | --- | ----------------- | --- | --- |
Small problems can be repaired directly at the maintenance station. If the maintenance
describing behavior that depends on
station cannot solve the problem, the product is sent to the maintenance regional
headquarters (if in US or EU) or to the maintenance main headquarters (otherwise).
sequences of events or stimuli
If the maintenance regional headquarters cannot solve the problem, the product is sent to
the maintenance main headquarters.
Example: UML state diagrams Maintenance is suspended if some components are not available.
Once repaired, the product is returned to the customer.
Example: coverage
(c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 5 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 6
0
NO
Maintenance
…to a test suite
|     |     |     |     |     |     |         | t            |     | b r e q       |                     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | ------------- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | pick up | s t  a       | ion | y   p u e     |                     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |         | q u e s ta t | [ U | S h o n s t   | return …to a finite |     |     |     |     |     |     |     |
TC1 0 2 4 1 0 r e n c e   ) reiruoc sserpxe yb ro (   o r e   o
|     |     |     |     |     |     |     | n a n ty           | noitats ecnanetniam )rebmun tcartnoc( c o | n E U r   w        |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | ----------------------------------------- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | main t e w a r r a |                                           | t ra   r e s e b   |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     | o                  |                                           | c t   n i d e      |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     | (n                 |  ta tseuqer                               | u m n t]           |     |     |     |     |     |     |     |     |
b e state
|     |     |     |     |     | 1   |     |     |     | r ) |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
|     |       |       |     |     | Wait for  |     Maintenance |     |     | 3   |          |     |     |     |     |     |     |     |
| --- | ----- | ----- | --- | --- | --------- | --------------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
| TC2 | 0 5 2 | 4 5 6 | 0   |     |           |                 |     |     |     | Wait for |     |     |     |     |     |     |     |
returning (no warranty) pick up Meaning: From state 0 to state
machine…
in
|     |       |       |     |     |          | etamitse | c on v a |     |         |     |     |     |     |     | 2 to state 4 to state 1 to state 0 |     |     |
| --- | ----- | ----- | --- | --- | -------- | -------- | -------- | --- | ------- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- |
|     |       |       |     |     | reje     | stsoc    | l id     |     |         |     |     |     |     |     |                                    |     |     |
|     |       |       |     |     |          |          | nu t r a |     |         |     | TC1 | 0 2 | 4 1 | 0   |                                    |     |     |
|     |       |       |     |     | ct estim |          | m c t    |     | pick up |     |     |     |     |     |                                    |     |     |
| TC3 | 0 3 5 | 9 6 0 |     |     |          |          | b e      |     |         |     |     |     |     |     |                                    |     |     |
r
ate
|     |       |       |       |     |     | 4          |             | 5 Repair      |                   | 6        |     |     |     |     |     |     |     |
| --- | ----- | ----- | ----- | --- | --- | ---------- | ----------- | ------------- | ----------------- | -------- | --- | --- | --- | --- | --- | --- | --- |
|     |       |       |       |     |     | Wait for   | accept      |               |                   |          |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            |             | (maintenance  | repair completed  | Repaired | TC2 | 0 5 | 2 4 | 5 6 | 0   |     |     |
|     |       |       |       |     |     | acceptance | estimate    |               |                   |          |     |     |     |     |     |     |     |
| TC4 | 0 3 5 | 7 5 8 | 7 8 9 | 6 0 |     |            |             | station)      |                   |          |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            | mponent (a) | (Uun          |                   |          |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            |             | S a b         | successful repair |          |     |     |     |     |     |     |     |
|     |       |       |       |     |     |            |             |  or E le      |                   |          | TC3 | 0 3 | 5 9 | 6 0 |     |     |     |
  t
|     |     |     |     |     |     |     |         | U                  | o   re  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | lack co |   r                |         |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         | c o m p o n e n t  | e s p a |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         |                    | i d ir  |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         | a r riv e s   (a ) | en      |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |         |                    | t )     | air |     |     |     |     |     |     |     |
ep
|     |     |     |     |     |     |           |                    |     |            | ul r | TC4 | 0 3 | 5 7 | 5 8 | 7   | 8 9 6 | 0   |
| --- | --- | --- | --- | --- | --- | --------- | ------------------ | --- | ---------- | ---- | --- | --- | --- | --- | --- | ----- | --- |
|     |     |     |     |     |     | 7         |                    |     | 8 Repair   | ssf  |     |     |     |     |     |       |     |
|     |     |     |     |     |     | Wait for  | lack component (b) |     | (regional  |      |     |     |     |     |     |       |     |
e
|     |     |     |     |     |     | component |     |     |               | cc  |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |           |     |     | headquarters) | su  |     |     |     |     |     |     |     |
component
unable to
|     |     |     |     |     |         |                      | la arrives (b) |     | repair |     |     |     |     |             |                  |                     |     |
| --- | --- | --- | --- | --- | ------- | -------------------- | -------------- | --- | ------ | --- | --- | --- | --- | ----------- | ---------------- | ------------------- | --- |
|     |     |     |     |     |         |                      | c              |     |        |     |     |     |     | I s  t hi s |   a  t h o r o u | g h  t e st suite?  |     |
|     |     |     |     |     | u n a b | le   to  r e p a i r | k  c           |     |        |     |     |     |     |             |                  |                     |     |
o m
(not  U S   o r  E U   r e si d ent) ponent (c) H o w   c a n   w e   ju d g e ?
10/10 = 100% state coverage
c o m p o n e n t
a r ri v e s   ( c )
9 Repair
| 17/20 = 85% transition coverage |     |     |     |     |     |     |     |     | (main  |     |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
(c) 2007 Mauro Pezzè & Michal Young headquarters)  Ch 14, slide 7 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 8
11

From an informal specification…
Maintenance: The Maintenance function records the history of items undergoing
maintenance.
If the product is covered by warranty or maintenance contract, maintenance can be
Multiple choices in the first step
requested either by calling the maintenance  toll free number, or through the web site, or
|     |     |     |     |     |     |     |     |     |     |     |     |     | by bringing the item to a designated maintenance station. |     |     |     |     | ... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
If the maintenance is requested by phone or web site and the customer is a US or EU
resident, the item is picked up at the customer site, otherwise, the customer shall ship the
Deriving test cases from finite state
item with an express courier.
If the maintenance contract number provided by t.h..e  dceustteormmeirn ies  nthote v paloids,s tihbei liittieems follows
machines
the procedure for items not covered by warranty.
for the next step ...
If the product is not covered by warranty or maintenance contract, maintenance can be
requested only by bringing the item to a maintenance station. The maintenance station
informs the customer of the estimated costs for repair. Maintenance starts only when the
customer accepts the estimate.
A common kind of model for
|     |     |     |     |     |     |     |     |     |     |     |     |     | If the customer does not accept the estimate, the product is returned to the customer. |     |     |     | ... and so on ... |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------------------------------- | --- | --- | --- | ----------------- | --- | --- |
Small problems can be repaired directly at the maintenance station. If the maintenance
describing behavior that depends on
station cannot solve the problem, the product is sent to the maintenance regional
headquarters (if in US or EU) or to the maintenance main headquarters (otherwise).
sequences of events or stimuli
If the maintenance regional headquarters cannot solve the problem, the product is sent to
the maintenance main headquarters.
Example: UML state diagrams Maintenance is suspended if some components are not available.
Once repaired, the product is returned to the customer.
Path sensitivity
(c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 5 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 6
0
NO
| Transition coverage |     |     | assumes  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Maintenance
…to a test suite
|            |                    |       |     |      |     |         |                | t           | b                                           | r e q         |        |              |     |     |     |     |     |     |     |
| ---------- | ------------------ | ----- | --- | ---- | --- | ------- | -------------- | ----------- | ------------------------------------------- | ------------- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- |
| that       | transitions depend |       |     | only |     | pick up | s t  a         | ion         | y   p                                       | u e           |        |              |     |     |     |     |     |     |     |
|            |                    |       |     |      |     |         | q u e          | s ta t      | [ U S                                       | h o n s t     | return | …to a finite |     |     |     |     |     |     |     |
|            |                    |       |     |      |     |         | r e n c e      |   )         | reiruoc sserpxe yb ro (   o r               | e   o         |        |              |     |     |     |     |     |     |     |
|            |                    |       |     |      |     |         | n a            | n ty        | noitats ecnanetniam )rebmun tcartnoc( c o n | E U r   w     |        |              |     |     |     |     |     |     |     |
|            |                    |       |     |      |     |         | main t e w a r | r a         | t ra                                        |   r e s e b   |        |              |     |     |     |     |     |     |     |
|            |                    |       |     |      |     |         | o              |             | c                                           | t   n i d e   |        |              |     |     |     |     |     |     |     |
| on current |                    | state |     |      |     |         | (n             |  ta tseuqer |                                             | u m n t]      |        |              |     |     |     |     |     |     |     |
|            |                    |       |     |      |     |         |                |             |                                             | b e           |        | state        |     |     |     |     |     |     |     |
|            |                    |       |     |      | 1   |         |                |             |                                             | r )           |        |              |     |     |     |     |     |     |     |
2
|     |     |     |     |     | Wait for  |     Maintenance |     |     |     | 3   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Wait for
returning (no warranty) pick up Meaning: From state 0 to state
|     | not on path | to reach |     | the state |     |     |     |     |     |     |     | machine… |     |     |     |     |     |     |     |
| --- | ----------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
in
|     |     |     |     |     |          | etamitse | c on | v a   |     |         |     |     |     |     |     |     | 2 to state 4 to state 1 to state 0 |     |     |
| --- | --- | --- | --- | --- | -------- | -------- | ---- | ----- | --- | ------- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- |
|     |     |     |     |     | reje     | stsoc    |      | l id  |     |         |     |     |     |     |     |     |                                    |     |     |
|     |     |     |     |     |          |          | nu   | t r a |     |         |     |     | TC1 | 0 2 | 4 1 | 0   |                                    |     |     |
|     |     |     |     |     | ct estim |          | m    | c t   |     | pick up |     |     |     |     |     |     |                                    |     |     |
b e
r
ate
|            |     |      |     |     |     | 4          |          | 5 Repair      |     |                  | 6        |     |     |     |     |     |     |     |     |
| ---------- | --- | ---- | --- | --- | --- | ---------- | -------- | ------------- | --- | ---------------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
|            |     |      |     |     |     | Wait for   | accept   |               |     |                  |          |     |     |     |     |     |     |     |     |
|            |     |      |     |     |     |            |          | (maintenance  |     | repair completed | Repaired |     | TC2 | 0 5 | 2 4 | 5 6 | 0   |     |     |
| Not always |     | true |     |     |     | acceptance | estimate |               |     |                  |          |     |     |     |     |     |     |     |     |
station)
|     |                               |     |     |     |     |     |     | mponent (a) | (Uun     |                   |     |     |     |     |     |     |     |     |     |
| --- | ----------------------------- | --- | --- | --- | --- | --- | --- | ----------- | -------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |                               |     |     |     |     |     |     |             | S a b    | successful repair |     |     |     |     |     |     |     |     |     |
|     |                               |     |     |     |     |     |     |             |  or E le |                   |     |     | TC3 | 0 3 | 5 9 | 6 0 |     |     |     |
|     | e.g. (a), (b), (c) in state 7 |     |     |     |     |     |     |             |   t      |                   |     |     |     |     |     |     |     |     |     |
U o   re
|     |     |     |     |     |     |     | lack co |               |   r         |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |         | c o m p o n e | n t e s p a |     |     |     |     |     |     |     |     |     |     |
i d ir
|     |                |     |          |        |     |     |     | a r riv e s   | (a ) en |     |     |     |     |     |     |     |     |     |     |
| --- | -------------- | --- | -------- | ------ | --- | --- | --- | ------------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | A flaw, should |     | be three | states |     |     |     |               | t       | )   | air |     |     |     |     |     |     |     |     |
ep
|     |     |     |     |     |     |           |     |                    |     |            | ul r |     | TC4 | 0 3 | 5 7 | 5 8 | 7   | 8 9 6 | 0   |
| --- | --- | --- | --- | --- | --- | --------- | --- | ------------------ | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | ----- | --- |
|     |     |     |     |     |     | 7         |     |                    | 8   | Repair     | ssf  |     |     |     |     |     |     |       |     |
|     |     |     |     |     |     | Wait for  |     | lack component (b) |     | (regional  |      |     |     |     |     |     |     |       |     |
e
|     |     |     |     |     |     | component |     |     |               |     | cc  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |           |     |     | headquarters) |     | su  |     |     |     |     |     |     |     |     |
component
unable to
|     |     |     |     |     |     |     | la  | arrives (b) |     | repair |     |     |     |     |     |             |                  |                     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------ | --- | --- | --- | --- | --- | ----------- | ---------------- | ------------------- | --- |
|     |     |     |     |     |     |     | c   |             |     |        |     |     |     |     |     | I s  t hi s |   a  t h o r o u | g h  t e st suite?  |     |
Needs path-sensitive criteria u n a b le   to  r e p a i r k  c
o m
(not  U S   o r  E U   r e si d ent) ponent (c) H o w   c a n   w e   ju d g e ?
c o m p o n e n t
a r ri v e s   ( c )
9 Repair
(main
(c) 2007 Mauro Pezzè & Michal Young headquarters)  Ch 14, slide 7 (c) 2007 Mauro Pezzè & Michal Young  Ch 14, slide 8
12

Path-sensitive criteria
Single state path coverage:
traverse each subpath that reaches states at most once
Single transition path coverage:
traverse each subpath that reaches transitions at most
once
Boundary interior loop coverage:
traverse each distinct loop the minimum, an
intermediate, and the maximum or a large number of
times
The most common
13

Decision structures
A representation of a
function
result = F(conditions)
n conditions
=> 2n possible combinations
Decision tables
Decision trees
Flow charts
Treat as Boolean expressions
Decisions, conditions
14

Example: specification
Pricing: The pricing function determines the adjusted price of a configuration
for a particular customer.
The scheduled price of a configuration is the sum of the scheduled price of
the model and the scheduled price of each component in the configuration. The
adjusted price is either the scheduled price, if no discounts are applicable, or the
scheduled price less any applicable discounts.
There are three price schedules and three corresponding discount
schedules, Business, Educational, and Individual.
….
Educational prices: The adjusted price for a purchase charged to an educational
account in good standing is the scheduled price from the educational price
schedule. No further discounts apply.
…
Special-price non-discountable offers: Sometimes a complete configuration is
offered at a special, non-discountable price. When a special, non-discountable
price is available for a configuration, the adjusted price is the non-discountable
price or the regular price after any applicable discounts, whichever is less
15

Example: decision table
|          |     |     | Business |     |     |     | Educ |     | Individual |     |
| -------- | --- | --- | -------- | --- | --- | --- | ---- | --- | ---------- | --- |
| EduAc    | - - | - - | - -      | - - | - - | - - |      |     |            |     |
|          |     |     |          |     |     |     | T T  | F F | F F        | F F |
| BusAc    | T T | T T | T T      | T T | T T | T T | - -  | F F | F F        | F F |
| CP > CT1 | F F | T T | F F      | T T | - - | - - | - -  | F F | T T        | - - |
| YP > YT1 | F F | F F | T T      | T T | - - | - - | - -  | - - | - -        | - - |
| CP > CT2 | - - | F F | - -      | - - | T T | - - | - -  | - - | F F        | T T |
| YP > YT2 | - - | - - | F F      | - - | - - | T T | - -  | - - | - -        | - - |
| SP > Sc  | F T | - - | - -      | - - | - - | - - | F T  | F T | - -        | - - |
| SP > T1  | - - | F T | F T      | - - | - - | - - |      |     |            |     |
|          |     |     |          |     |     |     | - -  | - - | F T        | - - |
| SP > T2  | - - | - - | - -      | F T | F T | F T | - -  | - - | - -        | F T |
Out ND SP T1 SP T1 SP T2 SP T2 SP T2 SP Edu SP ND SP T1 SP T2 SP
| EduAc    | Educational account                               |     |     |     |     | Edu | Educational price |     |     |     |
| -------- | ------------------------------------------------- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- |
| BusAc    | Business account                                  |     |     |     |     | ND  | No discount       |     |     |     |
| CP > CT1 | Current purchase greater than threshold 1         |     |     |     |     | T1  | Tier1             |     |     |     |
| YP > YT1 | Year cumulative purchase greater than threshold 1 |     |     |     |     | T2  | Tier 2            |     |     |     |
CP > CT2 Currentpurchasegreaterthanthreshold2 SP Special Price
| YP > YT2 | Year cumulative purchase greater than threshold 2 |     |     |     |     |     |     |     |     |     |
| -------- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SP > Sc  | Special Price better than scheduled price         |     |     |     |     |     |     |     |     |     |
| SP > T1  | Special Price better than tier 1                  |     |     |     |     |     |     |     |     |     |
16
| SP > T2 | Special Price better than tier 2 |     |     |     |     |     |     |     |     |     |
| ------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Example: decision table
"-" = don't care
|     |       | 1   | 2 3 | 4 5 | 6 7 | 8   |
| --- | ----- | --- | --- | --- | --- | --- |
|     | EduAc | T   | T F | F F | F F | F   |
|     | BusAc | -   | - F | F F | F F | F   |
Completeness: every
|     | CP > CT1 | -   | - F | F T | T - | -   |
| --- | -------- | --- | --- | --- | --- | --- |
(possible) combination
|     | YP > YT1 | -   | - - | - - | - - | -   |
| --- | -------- | --- | --- | --- | --- | --- |
is covered
|     | CP > CT2 | -   | - - | - F | F T | T   |
| --- | -------- | --- | --- | --- | --- | --- |
Consistency: no
|                         | YP > YT2 | -   | - -   | - -   | - -   | -   |
| ----------------------- | -------- | --- | ----- | ----- | ----- | --- |
| combination is covered  | SP < Sc  | F   | T F   | T -   | - -   | -   |
| twice                   | SP < T1  | -   | - -   | - F   | T -   | -   |
|                         | SP < T2  | -   | - -   | - -   | - F   | T   |
|                         | pricing  | udE |       |       |       |     |
|                         |          |     | PS DN | PS 1T | PS 2T | PS  |
17

Example: with constraints
| Restrict possible combinations |     |       | 1 2 | 3 4 | 5 6 | 7 8 |
| ------------------------------ | --- | ----- | --- | --- | --- | --- |
|                                |     | EduAc | T T | F F | F F | F F |
at-most-one (EduAc, BusAc)
|     |     | BusAc | - - | F F | F F | F F |
| --- | --- | ----- | --- | --- | --- | --- |
at-most-one (YP ≤ YT1, YP > YT2)
|     |     | CP > CT1 | - - | F F | T T | - - |
| --- | --- | -------- | --- | --- | --- | --- |
at-most-one (CP ≤ CT1, CP > CT2)
|     |     | YP > YT1 | - - | - - | - - | - - |
| --- | --- | -------- | --- | --- | --- | --- |
at-most-one (SP ≤ T1, SP > T2)
|            |          | CP > CT2 | - - | - -   | F F   | T T   |
| ---------- | -------- | -------- | --- | ----- | ----- | ----- |
| YP > YT2 ⇒ | YP > YT1 |          |     |       |       |       |
| CP > CT2 ⇒ | CP > CT1 | YP > YT2 | - - | - -   | - -   | - -   |
| SP > T2 ⇒  | SP > T1  |          |     |       |       |       |
|            |          | SP < Sc  | F T | F T   | - -   | - -   |
|            |          | SP < T1  | - - | - -   | F T   | - -   |
|            |          | SP < T2  | - - | - -   | - -   | F T   |
|            |          | pricing  | udE |       |       |       |
|            |          |          | PS  | DN PS | 1T PS | 2T PS |
18

Covering decision structures
Apply condition/decision-based criteria
Basic condition coverage:
a test case for each column
Compound condition coverage:
a test case for each (possible) combination of basic
conditions
Modified condition/decision coverage (MC/DC):
add columns that differ in one input row and in outcome,
merge compatible columns,
a test case specification for each column
19

Example: MC/DC
|     | 1 1' 1'' | 2 2' 2'' | 3 3' 3'' | 3''' 3'''' | 4 … | 5 … | 6 … | 7 … 8 … |
| --- | -------- | -------- | -------- | ---------- | --- | --- | --- | ------- |
1' covered by 3
| EduAc | T F | T T F T | F T | F F | F F | F   | F   | F F |
| ----- | --- | ------- | --- | --- | --- | --- | --- | --- |
1'' = 2
| BusAc | - - | - - - - | F F | T F | F F | F   | F   | F F |
| ----- | --- | ------- | --- | --- | --- | --- | --- | --- |
2' covered by 4
2'' = 1
| CP > CT1 | - - | - - - - | F F | F T | F F | T   | T   | - - |
| -------- | --- | ------- | --- | --- | --- | --- | --- | --- |
3' covers 1
| YP > YT1 | - - | - - - - | - - | - - | - - | -   | -   | - - |
| -------- | --- | ------- | --- | --- | --- | --- | --- | --- |
3'' covers 1'
| CP > CT2 | - - | - - - - | - - | - - | - - | F   | F   | T T |
| -------- | --- | ------- | --- | --- | --- | --- | --- | --- |
3''' covers 1',
| YP > YT2 | - - | - - - - | - - | - - | - - | -   | -   | - - |
| -------- | --- | ------- | --- | --- | --- | --- | --- | --- |
merge with 5
3'''' = 4
| SP < Sc | F F | T T T F | F F | F F | T T | -   | -   | - - |
| ------- | --- | ------- | --- | --- | --- | --- | --- | --- |
| SP < T1 | - - | - - - - | - - | - - | - - | F   | T   | - - |
| SP < T2 | - - | - - - - | - - | - - | - - | -   | -   | F T |
pricing
|     | udE |     | DN  |     |     |     |     |       |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|     |     | PS  |     |     | PS  | 1T  | PS  | 2T PS |
|     | - - | - - | - - | - - |     |     |     |       |
20

Grammars
|     | <Model> | ::= <modelNumber> <compSequence> <optCompSequence> |     |     |
| --- | ------- | -------------------------------------------------- | --- | --- |
<compSequence> ::= <Component> <compSequence> | empty
<optCompSequence> ::= <OptionalComponent> <optCompSequence> | empty
|                     | <Component> | ::= <ComponentType> <ComponentValue> |     |     |
| ------------------- | ----------- | ------------------------------------ | --- | --- |
| <OptionalComponent> |             | ::= <ComponentType>                  |     |     |
| <modelNumber>       |             | ::= string                           |     |     |
<ComponentType> ::= string
<ComponentValue> ::= string
| Grammars | are good      | for structured |      | inputs |
| -------- | ------------- | -------------- | ---- | ------ |
| varying  | and unbounded |                | size |        |
recursive structure
Examples:
| textual | inputs                      |     |     |     |
| ------- | --------------------------- | --- | --- | --- |
| Trees   | (incl. XML, HTML, programs) |     |     |     |
21

Grammar-based testing
| Test cases |     |     | are strings | generated |     |     | from the grammar |     |
| ---------- | --- | --- | ----------- | --------- | --- | --- | ---------------- | --- |
Production coverage:
| each     |     | production must be used |           |           |     | at  | least | once  |
| -------- | --- | ----------------------- | --------- | --------- | --- | --- | ----- | ----- |
| Boundary |     |                         | condition | coverage: |     |     |       |       |
each recursive production must be used (min, min+1, max–1, max)
times,
| where |                                | min   | and max     | are set for each |         |                         |                        | production            |
| ----- | ------------------------------ | ----- | ----------- | ---------------- | ------- | ----------------------- | ---------------------- | --------------------- |
|       | Similar                        |       | to boundary | interior         |         | path                    |                        |                       |
| Tests |                                | cases | generated   | depend           |         | on generation strategy: |                        |                       |
|       | productions with non-terminals |       |             |                  |         |                         | first ⇒                | few, large test cases |
|       | productions with terminals     |       |             |                  | first ⇒ |                         | many, small test cases |                       |
22

Example: specification
Check Configuration: Check the validity of a computer configuration. The
parameters of check configuration are:
Model: A model identifies a specific product and determines a set of
constraints on available components. Models are characterized by logical slots
for components, which may or may not be implemented by physical slots on a
bus. Slots may be required or optional. Required slots must be assigned with a
suitable component to obtain a legal configuration, while optional slots may
be left empty or filled depending on the customers' needs
Set of components: set of (slot, component) pairs, corresponding to the
required and optional slots of the model. A component is a choice that be
varied within a model, and which is not designed to be replaced by the end
user. Available components and a default for each slot is determined by the
model. The special value empty is allowed (and may be the default selection)
for optional slots. In addition to being compatible or incompatible with a
particular model and slot, individual components may be compatible or
incompatible with each other.
23

Example: grammar
<Model> ::= <modelNumber> <compSequence> <optCompSequence>
<compSequence> ::= <Component> <compSequence> | empty
<optCompSequence> ::= <OptionalComponent> <optCompSequence> | empty
<Component> ::= <ComponentType> <ComponentValue>
<OptionalComponent> ::= <ComponentType>
<modelNumber> ::= string
<ComponentType> ::= string
<ComponentValue> ::= string
24

Example: with names and limits
| Model |     |     | <Model> | ::= <modelNumber> <compSequence>  |
| ----- | --- | --- | ------- | --------------------------------- |
<optCompSequence>
| compSeq1 | [0, 16] |     |     | ::= <Component> <compSequence> |
| -------- | ------- | --- | --- | ------------------------------ |
<compSequence>
| compSeq2 |     | <compSequence> |     | ::= empty |
| -------- | --- | -------------- | --- | --------- |
optCompSeq1 [0, 16] ::= <OptionalComponent> <optCompSequence>
<optCompSequence>
| optCompSeq2 |     |     |     | ::= empty |
| ----------- | --- | --- | --- | --------- |
<optCompSequence>
| Comp    |     | <Component> |     | ::= <ComponentType> <ComponentValue> |
| ------- | --- | ----------- | --- | ------------------------------------ |
| OptComp |     |             |     | ::= <ComponentType>                  |
<OptionalComponent>
| modNum |     |     |     | ::= string |
| ------ | --- | --- | --- | ---------- |
<modelNumber>
| CompTyp |     | <ComponentType> |     | ::= string |
| ------- | --- | --------------- | --- | ---------- |
| CompVal |     |                 |     | ::= string |
<ComponentValue>
25

Example: test cases
| Model |     | ::= <modelNumber> <compSequence>  |
| ----- | --- | --------------------------------- |
<Model>
<optCompSequence>
compSeq1 [0, 16] <compSequence> ::= <Component> <compSequence>
| compSeq2 |     | ::= empty |
| -------- | --- | --------- |
<compSequence>
optCompSeq1 [0, 16] ::= <OptionalComponent> <optCompSequence>
<optCompSequence>
| optCompSeq2 |     | ::= empty |
| ----------- | --- | --------- |
<optCompSequence>
| Comp |     | ::= <ComponentType> <ComponentValue> |
| ---- | --- | ------------------------------------ |
<Component>
| OptComp |     | ::= <ComponentType> |
| ------- | --- | ------------------- |
<OptionalComponent>
| modNum  | <modelNumber>   | ::= string |
| ------- | --------------- | ---------- |
| CompTyp | <ComponentType> | ::= string |
| CompVal |                 | ::= string |
<ComponentValue>
“Mod000”
Covers Model, compSeq1[0], compSeq2, optCompSeq1[0], optCompSeq2, modNum
“Mod000 (Comp000, Val000) (OptComp000)”
Covers Model, compSeq1[1], compSeq2, optCompSeq2[1], optCompSeq2, Comp,
OptComp, modNum, CompTyp, CompVal
Etc…
26

Grammar vs. Combinatorial Testing
Combinatorial testing:
good for mostly independent parameters
A few constraints are OK
But complex constraints are hard
Grammar testing:
good for sequences and nested structure
Relations among different parts may be difficult to
describe and exercise systematically
27

TESTING OBJECT-ORIENTED
SOFTWARE
28

15.2
Object-Oriented Software
Characteristics that impact testing:
• State dependent behavior
Objects have state
• Encapsulation
Test oracles may need access to private data
• Inheritance
Effect of new methods on inherited methods
• Polymorphism and dynamic binding
One call may be bound to different methods
• Abstract and generic classes
Must instantiate to test
• Exception handling
Non-local, dynamic control flow
• Concurrency
Often necessary (GUI), deadlocks, races, scheduling
29

Unit and integration testing
Procedural software: unit = single function or
procedure
or more often, one or more intertwined functions or
procedures
Object oriented software: unit = single class
or (small) cluster of strongly related classes (e.g.
exceptions)
unit testing = intra-class testing
integration testing = inter-class testing
dealing with single methods is usually too expensive
30

15.4/5
Intraclass State Machine Testing
Basic ideas:
• Objects have a state
• Methods calls are state transitions
• Test cases are sequences of method calls
State machine model can be derived
from specification (functional testing),
from code (structural testing), or both
Model-based testing, state/transition coverage
32

Example: specification
Slot: represents a slot of a computer model.
.... slots can be bound or unbound. Bound slots are assigned a compatible
component, unbound slots are empty. Class slot offers the following services:
Install: slots can be installed on a model as required or optional.
...
Bind: slots can be bound to a compatible component.
...
Unbind: bound slots can be unbound by removing the bound component.
IsBound: returns the current binding, if bound; otherwise returns the special
value empty.
Three states: Not_installed, Unbound, Bound
Four transitions: install, bind, unbind, isBound
33

Example: FSM and test cases
Deriving an FSM and test cases
isBound
incorporate
unBind
0 1 2
Not present Unbound Bound
isBound
bind
unBind
• TC-1: incorporate, isBound, bind, isBound
TC-1: incorporate, isBound, bind, isBound
TC-2: incorporate, unBind, bind, unBind, isBound
• TC-2: incorporate, unBind, bind, unBind, isBound
34
(c) 2007 Mauro Pezzè & Michal Young
Thursday, January 17, 13

15.7
Structural Testing of Classes
As for procedural software,
start with functional testing (from specifications),
then complete with structural testing (from the
code)
Difficulty: objects have state
Methods must be called in right order
Analysis in a single method is not adequate
Need sequences of method calls
39

Intraclass control
flow graph
Each method +
Node for class +
Edges class → method,
method → class
=> control flow
through sequences of
method calls
40

Interclass structural testing
DU pair structural testing:
Working bottom-up in dependence hierarchy
Leaf classes, then classes that use leaf classes, ...
Classify each method:
inspectors: use, but do not modify, object state
modifiers: modify, but not use, object state
inspector/modifiers: use and modify object state
Treating a whole object as a variable (not each field)
Treat inspector calls as uses, modifier calls as defs
41

Oracles
Test oracles must be able to check the
correctness of a test execution
• Correct output: OK, can be checked
• Correct new state: not accessible,
encapsulation
42

Accessing the state
Intrusive approach:
use language constructs (C++ friend classes)
add inspector methods
– Breaks encapsulation
– May produce undesired results
Equivalent scenarios approach:
generate equivalent sequences of method calls
compare the final states of the objects
43

Equivalent Scenarios: Example
EQUIVALENT
selectModel(M1)
selectModel(M2)
addComponent(S1,C1)
addComponent(S1,C1)
addComponent(S2,C2)
isLegalConfiguration()
isLegalConfiguration()
deselectModel()
selectModel(M2)
addComponent(S1,C1)
NON EQUIVALENT
isLegalConfiguration()
selectModel(M2)
addComponent(S1,C1)
addComponent(S2,C2)
isLegalConfiguration()
44

Polymorphism:
combinatorial explosion problem
abstract class Credit {
...
abstract boolean validateCredit( Account a, int amt, CreditCard c);
...
}
EduCredit USAccount VISACard
BizCredit UKAccount AmExpCard
IndividualCredit EUAccount StoreCard
JPAccount
OtherAccount
The combinatorial problem: 3 x 5 x 3 = 45 possible
combinations
of dynamic bindings (just for this one method!)
45

The combinatorial approach
| Account   | Credit    | creditCard |
| --------- | --------- | ---------- |
| USAccount | EduCredit | VISACard   |
Pairwise testing:
| USAccount | BizCredit | AmExpCard  |
| --------- | --------- | ---------- |
test cases that
| USAccount | individualCredit | ChipmunkCard |
| --------- | ---------------- | ------------ |
cover all pairwise
| UKAccount | EduCredit | AmExpCard |
| --------- | --------- | --------- |
| UKAccount | BizCredit | VISACard  |
combinations of
| UKAccount | individualCredit | ChipmunkCard |
| --------- | ---------------- | ------------ |
dynamic bindings
| EUAccount    | EduCredit        | ChipmunkCard |
| ------------ | ---------------- | ------------ |
| EUAccount    | BizCredit        | AmExpCard    |
| EUAccount    | individualCredit | VISACard     |
| JPAccount    | EduCredit        | VISACard     |
| JPAccount    | BizCredit        | ChipmunkCard |
| JPAccount    | individualCredit | AmExpCard    |
| OtherAccount | EduCredit        | ChipmunkCard |
| OtherAccount | BizCredit        | VISACard     |
| OtherAccount | individualCredit | AmExpCard    |
46

15.10
Inheritance
class Child extends Parent
When testing Child
We would like to test only what is needed
Not what has been tested in Parent
Any method whose behavior may have changed
even accidentally!
47

15.11
Testing generic classes
class PriorityQueue<Elem Implements
Comparable> {...}
PriorityQueue<Customers>
PriorityQueue<Tasks>
We can test only instantiations, not the generic class
we may not know what instantiations
Testing can be broken into two parts
Showing that some instantiation is correct
showing that all instantiations behave consistently
49

15.12
Exception handling
void addCustomer(Customer theCust) {
customers.add(theCust);
}
public static Account
newAccount(...) throws InvalidRegionException
{
Account thisAccount = null;
String regionAbbrev = Regions.regionOfCountry(
mailAddress.getCountry());
if (regionAbbrev == Regions.US) {
thisAccount = new USAccount();
} else if (regionAbbrev == Regions.UK) {
....
} else if (regionAbbrev == Regions.Invalid) {
throw new InvalidRegionException(mailAddress.getCountry());
}
...
}
Exceptions:
Implicit control flows
May be handled by different handlers
50

Testing exception handling
Impractical to treat exceptions like normal flow
Too many flows:
every exception source × every exception handler
array subscripts, divisions, pointer references, …
many actually impossible
Program error exceptions:
test to prevent them, not to handle them
Explicit throws:
test w.r.t. every handler on call stack
51

Testing exception handlers
Local exception handlers:
Test the exception handler
Non-local exception handlers:
Difficult to determine all <source, handler> pairs
Design rule: if a method propagates an exception,
the method call should have no other effect
Test all sources, all handlers (but not all pairs)
52

Summary
Features of object-oriented languages and
programs impact testing
State, encapsulation, inheritance, polymorphism,
genericity, exceptions
but only at unit and integration levels
General principles are still applicable
Approaches for each issue are orthogonal
can be applied incrementally and independently
53

FAULT-BASED TESTING
54

How good are your tests?
| Functional |     | testing: |
| ---------- | --- | -------- |
in out
Are all specifications covered?
Structural testing:
Are all parts of the program covered?
| Will it     | find | all faults? |
| ----------- | ---- | ----------- |
| Fault-based |      | testing:    |
Are all (injected) faults covered?
55

Basic Assumptions
Judge how well a test suite finds real faults,
by measuring how well it finds seeded faults.
Valid if seeded faults
are representative of real faults
We need good fault models
56

Mutation testing
A mutation is a syntactic change (a seeded fault)
| Example:  change (i | < 0)  to (i | <= 0) |
| ------------------- | ----------- | ----- |
A mutant is a copy of a program with a mutation
valid mutant = syntactically correct
Run test suite on all the mutants
| A mutant is killed | if it fails | on at least one test case |
| ------------------ | ----------- | ------------------------- |
If many mutants are killed,
then the test suite is effective at finding real faults
57

Mutation testing assumptions
Competent programmer hypothesis:
Programs are nearly correct
Real faults are small variations from the correct
program
Mutants are reasonable models of real faults
Coupling effect hypothesis:
Tests that find simple faults
also find more complex faults
Even if mutants are only simple faults, a test
suite that kills mutants is good at finding
complex faults too
58

Mutation Operators
Syntactic change from legal program to legal
program
So: Specific to a programming language
Examples:
crp: constant for constant replacement
| (x < 5) |     | →   | (x < 12) |
| ------- | --- | --- | -------- |
ror: relational operator replacement
| (x <= | 5)  | →   | (x < 5) |
| ----- | --- | --- | ------- |
vie: variable initialization elimination
| int x = 5; |     | →   | int x; |
| ---------- | --- | --- | ------ |
59

|                       | Example: Mutation operators |     |             |     | in C |            |     |
| --------------------- | --------------------------- | --- | ----------- | --- | ---- | ---------- | --- |
| ID Operator           |                             |     | Description |     |      | Constraint |     |
| Operand Modifications |                             |     |             |     |      |            |     |
crp constant for constant replacement replace constant C1 with constant C2 C1 C2
≠
C X
scr scalar for constant replacement replace constant C with scalar variable X ≠
acr array for constant replacement replace constant C with array reference A[I] C ≠ A[I]
scr struct for constant replacement replace constant C with struct field S C S
≠
svr scalar variable replacement replace scalar variable X with a scalar variable Y X ≠ Y
csr constant for scalar variable replacement replace scalar variable X with a constant C X C
≠
X A[I]
asr array for scalar variable replacement replace scalar variable X with an array reference A[I] ≠
ssr struct for scalar replacement replace scalar variable X with struct field S X ≠ S
vie scalar variable initialization elimination remove initialization of a scalar variable
car constant for array replacement replace array reference A[I] with constant C A[I]≠C
sar scalar for array replacement replace array reference A[I] with scalar variable X A[I]≠C
cnr comparable array replacement replace array reference with a comparable array reference
sar struct for array reference replacement replace array reference A[I] with a struct field S A[I]≠S
Expression Modifications
| abs absolute | value insertion | replace | e by abs(e) |     |     | e < 0 |     |
| ------------ | --------------- | ------- | ----------- | --- | --- | ----- | --- |
aor arithmetic operator replacement replace arithmetic operator with arithmetic operator e 1ψe 2≠e 1φe
|                                   |     |                           |     | ψ                      | φ   |       | 2      |
| --------------------------------- | --- | ------------------------- | --- | ---------------------- | --- | ----- | ------ |
|                                   |     | replace logical connector |     | with logical connector |     | e 1ψe | ≠e 1φe |
| lcr logical connector replacement |     |                           |     | ψ                      | φ   | 2     | 2      |
ror relational operator replacement replace relational operator ψ with relational operator φ e 1ψe ≠e 1φe
|                              |     |              |          |     |     | 2   | 2   |
| ---------------------------- | --- | ------------ | -------- | --- | --- | --- | --- |
| uoi unary operator insertion |     | insert unary | operator |     |     |     |     |
cpr constant for predicate replacement replace predicate with a constant value
| Statement     | Modifications |        |             |     |     |     |     |
| ------------- | ------------- | ------ | ----------- | --- | --- | --- | --- |
| sdl statement | deletion      | delete | a statement |     |     |     |     |
sca switch case replacement replace the label of one case with another
| ses end block shift |     | move } one statement |     | earlier and later |     |     |     |
| ------------------- | --- | -------------------- | --- | ----------------- | --- | --- | --- |
60

Mutation Analysis
Steps:
• Select mutation operators
possibly selected classes of faults
• Generate mutants
by applying mutation operators to the program
• Distinguish mutants
execute all tests on program + all mutants
mutant i is killed if test(mutant i) ≠ test(program) for some test
Mutation score: # killed mutants / # total mutants
What can we learn from the living mutants?
61

How mutants survive
Two possible reasons:
• The mutant is equivalent to the original program
The mutation does not change the behaviour
The seeded fault is not really a fault
• Or the test suite is inadequate
The mutant could have been killed, but was not
Adding a test case for just this mutant is a bad idea!
We care about the real bugs, not the fakes!
62

Fault-based coverage
Fault-based coverage:
All non-equivalent mutants are killed by at least
one test case
Measure:
C = # killed mutants / # non-equivalent mutants
Fault
Equivalent mutants are hard to determine
undecidable in the worst case
63

Mutants for a + b > c
a + b > c
| a - b > c       | a - b >= c | a - b > 0     |     |
| --------------- | ---------- | ------------- | --- |
| a * b > c       | a - b < c  | ++a - b > c   |     |
| a / b > c       | a - b <= c | a - ++b > c   |     |
| a % b > c       | a - b = c  | a - b > ++c   |     |
| a > c           | a - b != c | --a - b > c   |     |
| b > c           | b - b > c  | a - --b > c   |     |
| abs(a) - b > c  | a - a > c  | a - b > --c   |     |
| a - abs(b) > c  | c - b > c  | ++(a - b) > c |     |
| a - b > abs(c)  | a - c > c  | --(a - b) > c |     |
| abs(a - b) > c  | a - b > a  | -a - b > c    |     |
| -abs(a) - b > c | a - b > b  | a - -b > c    |     |
| a - -abs(b) > c | a - b > c  | a - b > -c    |     |
| a - b > -abs(c) | 0 - b > c  | -(a - b) > c  |     |
| -abs(a - b) > c | a - 0 > c  | 0 > c         | 64  |
Thursday, January 17, 13

Mutation variants
Problem: There are lots of mutants
Grows with the square of program size
Running each test case on each mutant is expensive
Weak mutation: observe states of program and mutant,
kill as soon as a difference is found
do not wait for test completion
Meta-mutant: mutant with several seeded faults,
with mechanism to activate the mutants
check several mutants in one test run
Statistical mutation: create a random sample of mutants
OK for assessing a test suite
65

In real life ...
Fault-based testing is a widely used in
semiconductor manufacturing
Good fault models of typical manufacturing faults
E.g. “stuck-at-one” for a transistor
Design errors are more challenging (as in software)
Mutation testing is not widely used in industry
But plays a role in software testing research, to
compare effectiveness of testing techniques
66

When to Stop Testing
The more faults you have found,
the more faults likely remain!
When to stop?
When no faults (likely) remain
How to estimate how many faults remain?
67

How many fish?
A lake full of fish
N?
100
How many?
I cannot fish them all
Catch 100, tag them
Thursday, January 17, 13
Throw them back
68

How many fish?
Catch 200 again
40
N?
100
160
How many in the lake?
Assumption: same probability of catching tagged or untagged
% tagged caught ≈ % tagged total
Thursday, January 17, 13
| "#  | &## |     | $##×&## |       |
| --- | --- | --- | ------- | ----- |
| ≈   |     | 𝑁 ≈ |         | = 500 |
| $## | '   |     | "#      |       |
69

How many faults?
How many remaining (natural) faults N?
Intentionally seed S faults in the program
Run the tests
s discovered seeded faults
n discovered natural faults
Hypothesis: same effectiveness n / N = s / S
N = S . n / s
Confidence that N = 0 if n = 0 and s = S: S / (S + 1)
S = 10 → 91%, S = 49 → 98%
70

Independent Test Groups
| If we | don't | know typical |     | faults? |     |
| ----- | ----- | ------------ | --- | ------- | --- |
N
n2
| Split tests in two |        | groups E1, E2 |       |     |     |
| ------------------ | ------ | ------------- | ----- | --- | --- |
| n1                 | faults | detected      | by E1 |     |     |
n1
n12
| n2                        | faults | detected     | by E2   |           |          |
| ------------------------- | ------ | ------------ | ------- | --------- | -------- |
| n12                       | faults | detected     | by both | E1 and E2 |          |
| N                         | faults | in total     |         |           |          |
| Hypothesis: effectiveness |        |              |         | of E1 is  | the same |
| on all faults             |        | as on faults |         | detected  | by E2:   |
| n1 / N = n12 / n2         |        |              | =>      |           |          |
N  =  n1 . n2 / n12
71

Summary
Fault-based testing
Mutation testing: generate mutants,
Check that test suite kills mutants
Fault estimation: seed S faults, find s seeded + n
natural, N = n × S / s
72

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 14, 15, 16
73

Software Quality Assurance
5c – Test Execution
Charles Pecheur
Mar 2018
1

Test Execution
Test Execution
Scaffolding, stubs, drivers, harness
Test oracles
Testing activities
Unit testing
Integration testing
System testing
Acceptance testing
Regression testing
2

Automating Test Execution
Designing test cases is creative
Like any design activity
Software Test
Specs Design
Executing test cases
should be automatic
Program Test
Design Specs
Design once, execute many times
Test
Software
Execution
• Generate test cases
• Testing code: scaffolding
Test
• Testing results: oracles
Results
3

Test	  Case	  Generation
From	  Test	  Case	  Specifications	  to	  Test	  Cases
“a	  large	  positive	  number”	  →	   420023
“a	  sorted sequence,	  length >	  2”	  →	   [2,	  4,	  7,	  10]
Can	  be	  automated
| constraint  | solving    |           |              |           |
| ----------- | ---------- | --------- | ------------ | --------- |
| may         | require    | difficult | computations |           |
| e.g.	  all | conditions |           | along        | a	  path |
4

Scaffolding
Scaffolding:
code produced to support
development activities
especially testing
Not part of the product
May be temporary
Includes
Test harnesses
Drivers
Stubs
Image by Kevin Dooley under Creative Commons license

Harness, Driver and Stub
Test harness: environment in which the
component is tested
Harness
Ex: Software simulation of a hardware
Driver
device
calls
Tested
Test driver: calls the component
Component
Applies the test cases
calls
A “main” program for running a test
Stub
Test stubs: called by the component
Substitutes for called components
6

Controllability	  and	  Observability
| The	  scaffolding |     | must	  provide: |     |     |     |
| ------------------ | --- | ---------------- | --- | --- | --- |
Harness
control observe
Controllability:
Tested
| allow | to	  execute |     | test	  cases |     |     |
| ----- | ------------- | --- | ------------- | --- | --- |
Component
Observability:
| allow          | to	  judge | the	  outcome |     |                        | of	  tests |
| -------------- | ----------- | -------------- | --- | ---------------------- | ----------- |
| May	  require |             | additional     |     | interfaces,	  drivers |             |
7

Controllability & Observability: GUI
GUI input (MVC “Controller”)
We want
limited control
automated tests
Program
limited observation
GUI output (MVC “View”)
8

Controllability & Observability: GUI
GUI input (MVC “Controller”) Test driver
control
API
Program
Log behavior
observation
Capture wrapper
GUI output (MVC “View”)
9

Generic or Specific?
How general should scaffolding be?
Specific
• A driver and stubs for each test case
• Common code for the driver and test management
e.g. JUnit
• Support code to drive a large number of test cases from data
e.g. DDSteps
• Generate the data automatically from a more abstract model
Generic
A question of costs and re-­‐use
Just as for other kinds of software
10

Test Oracles
Did this test case succeed, or fail?
Oracle: software that determines whether a test
passed or failed
Better than manual checking
• More efficient
• More reliable
• More capable (e.g. timing, large data)
11

Partial	  Oracles
| Oracles	  should |     | ideally:   |           |     |            |     |
| ----------------- | --- | ---------- | --------- | --- | ---------- | --- |
| report	  PASS    |     | for	  all | correct   |     | executions | and |
| report	  FAIL    |     | for	  all | incorrect |     | executions |     |
Partial	  oracles:
| report	  PASS        |                           | for	  all	  correct	  executions   |             |     |                         | and |
| --------------------- | ------------------------- | ------------------------------------- | ----------- | --- | ----------------------- | --- |
| may                   | report	  PASS            |                                       | for	  some |     | incorrect	  executions |     |
| No	  false	  alarms |                           | (FAIL	  on	  correct	  executions) |             |     |                         |     |
| Several               | partial	  oracles	  may |                                       |             | be  | more	  effective	     |     |
| than                  | one	  complete           |                                       | oracle      |     |                         |     |
12

Types of Oracles
Comparison-­‐based oracle:
compare predicted and actual output
test case = (test input, expected output)
Most common but not the only approach!
Test cases are not always with a known expected output
e.g. find a route from A to B
Self-­‐checks:
checks in the program under test (assert)
no test output needed
Capture and replay:
capture first test run (input, output) then replay
for interactive programs, GUI
13

Comparison-­‐Based Oracle
Oracle compares actual to expected output,
reports if (actual = expected) then PASS else FAIL
Fine for a small number of hand-­‐generated test cases
E.g. JUnit test cases: assertEquals(actual, expected)

Self-­‐Checks as Oracle
Oracle as self-­‐checks in the program (assertions)
judge correctness without predicting results
+ Usable with large, automatically generated test suites
– Often only a partial check
e.g., structural invariants of data structures

Assertions	  as	  Oracle
| Invariants |                          | on	  data	  structures |                                                 |     |     |     |     |     |
| ---------- | ------------------------ | ------------------------ | ----------------------------------------------- | --- | --- | --- | --- | --- |
|            | e.g.                     | assert                   | 0	  <=	  size	  &&	  size	  <=	  a.length |     |     |     |     |     |
| Pre-­‐     | and	  post-­‐conditions |                          |                                                 |     |     |     |     |     |
|            | e.g.                     | assert                   | k	  !=	  null                                 |     | ;   |     |     |     |
v	  =	  dict.get(k)	  ;
|             |              | assert                                                                  | dict.contains(k,	  v)	  ; |                 |             |                         |              |              |
| ----------- | ------------ | ----------------------------------------------------------------------- | --------------------------- | --------------- | ----------- | ----------------------- | ------------ | ------------ |
| May	  need |              | to	  deal	  with                                                      |                             |                 | quantifiers |                         |              |              |
|             | e.g.         | for	  all	  (k,	  v),	  (k',	  v')	  in	  dict,	  k	  !=	  k' |                             |                 |             |                         |              |              |
|             | e.g.         | result                                                                  | is                          | the	  shortest |             | route	  from           |              | A	  to	  B |
|             | implement    |                                                                         | as	  iteration             |                 | ⇒           | does                    | not	  scale | well         |
|             | or	  sample |                                                                         | some                        | elements        |             | (partition	  testing!) |              |              |
16

Capture and Replay
Test Case Captured
Test Harness
Test Harness
Capture
Replay
Test Inputs Inputs
Outputs Compare Pass/Fail
Program Program
Under Test Under Test
Capture a manually run test case
sequence of inputs, outputs
Replay it automatically
with a comparison-­‐based oracle:
compare actual to captured outputs
Reusable only until a program change invalidates it
lifetime depends on abstraction level of input and output
17

TESTING ACTIVITIES
18

Program Testing
Need Product
Maintenance
Requirements definition Acceptance testing
System design System testing
Program design Integration testing
Program writing Unit testing
Code
19

Testing Activities
System System
tests delivery
20

Unit
Testing
Aka. module testing, component testing
Each program component
Testing
feed inputs, check valid outputs
Code reviews, analyses
check internal data structures, logic
21

Integration
Testing
Assemble components together
Check correct interaction
22

Function
Testing
The whole system
Check that the behaviour conforms
to functional requirement specifications
23

Performance
Testing
The whole system
Check that the behaviour conforms
to nonfunctional requirement specifications
24

Acceptance
Testing
The whole system
Test using the system with the customer
Check that the behaviour conforms
to (customer) requirement documentation
25

Installation
Testing
The system in its operational environment
Check that the system
performs properly in its environment
26

Unit	  Testing
|                | Module test | Integration test  | System test   |
| -------------- | ----------- | ----------------- | ------------- |
| Specification: | Module      | Interface specs,  | Requirements  |
|                | interface   | module breakdown  | specification |
Visible structure: Coding details Modular structure  — none —
(software architecture)
| Scaffolding  | Some | Often extensive | Some |
| ------------ | ---- | --------------- | ---- |
required:
| Looking for faults  | Modules | Interactions,  | System        |
| ------------------- | ------- | -------------- | ------------- |
| in:                 |         | compatibility  | functionality |
27

Unit	  Testing
| Goal:	  find | faults | in	  single	  components |
| ------------- | ------ | -------------------------- |
•
Examine	  the	  code: code	  reviews
| …	  and	  associated |     | specifications |
| ---------------------- | --- | -------------- |
•
Analyze the	  code:	  code	  analysis,	  proofs
| manually                      | or	  with | tools |
| ----------------------------- | ---------- | ----- |
| • Run the	  code:	  testing |            |       |
functional +	  structural	  (+	  OO	  /	  model	  /	  fault-­‐based)
28

Integration Testing
|                | Module test | Integration test  | System test   |
| -------------- | ----------- | ----------------- | ------------- |
| Specification: | Module      | Interface specs,  | Requirements  |
|                | interface   | module breakdown  | specification |
Visible structure: Coding details Modular structure  — none —
(software architecture)
| Scaffolding  | Some | Often extensive | Some |
| ------------ | ---- | --------------- | ---- |
required:
| Looking for faults  | Modules | Interactions,  | System        |
| ------------------- | ------- | -------------- | ------------- |
| in:                 |         | compatibility  | functionality |
29

Integration Faults
• Inconsistent interpretation of parameters or values
Example: Mixed units (meters/yards) in Martian Lander
• Violations of value domains, capacity, or size limits
Example: Buffer overflow
• Side effects on parameters or resources
Example: Conflict on (unspecified) temporary file
• Omitted or misunderstood functionality
Example: Inconsistent interpretation of web hits
• Nonfunctional properties
Example: Unanticipated performance issues
• Dynamic mismatches
Example: Incompatible polymorphic method calls
30

Integration Testing Strategies
Combine components together for testing
Consider the component hierarchy
by layers / uses
Possible strategies: bottom-­‐up, top-­‐down, combined
integration test plan
drives and is driven by
project build plan
31

Big-­‐Bang Integration
Everything integrated in one shot
An extreme and desperate approach
For small systems only
+ Does not need drivers and stubs
– Faults are hard to localize
– Interface faults are hard to distinguish
32

Structural and Functional Strategies
Structural orientation:
based on a hierarchical project structure
Top-­‐down, Bottom-­‐up, Sandwich, Backbone
Functional orientation:
based on application characteristics or features
Threads, Critical module
33

Bottom-­‐Up Integration
Useful if many general-­‐purpose utility routines,
reused components at lowest level
Needs drivers
– The top-­‐level components are tested last
most important, may reveal design bugs
+ Suitable for object-­‐oriented programs
34

Top-­‐Down Integration
Test the top-­‐level, controlling component first
Needs stubs
+ Allows test by external function
+ Major design faults or issues revealed early
+ Drivers not needed
– Stubs can be difficult to develop,
affects validity of the test
35

Modified Top-­‐Down Integration
Test components individually
before integrating components
+ Individual testing of interior components
– Needs stubs and drivers
36

Sandwich Integration
Combine bottom-­‐up and top-­‐down,
converge to target middle layer
+ Early test of top layer
+ No stubs for utility components in bottom layer
37

Modified Sandwich Integration
Test upper-­‐level components before merging
38

Comparison	  of
Structural	  Integration	  Strategies
Depends on	  system	  characteristics AND	  customer expectations
|                | Bottom- | Top-  | Modified  | Big-bang | Sandwich | Modified  |
| -------------- | ------- | ----- | --------- | -------- | -------- | --------- |
|                | up      | down  | top-down  |          |          | sandwich  |
| Integration    | Early   | Early | Early     | Late     | Early    | Early     |
| Time to basic  | Late    | Early | Early     | Late     | Early    | Early     |
working program
| Component drivers  | Yes | No  | Yes | Yes | Yes | Yes |
| ------------------ | --- | --- | --- | --- | --- | --- |
needed
| Stubs needed         | No     | Yes  | Yes    | Yes  | Yes    | Yes  |
| -------------------- | ------ | ---- | ------ | ---- | ------ | ---- |
| Work parallelism at  | Medium | Low  | Medium | High | Medium | High |
beginning
| Ability to test  | Easy | Hard | Easy | Easy | Medium | Easy |
| ---------------- | ---- | ---- | ---- | ---- | ------ | ---- |
particular paths
| Ability to plan and  | Easy | Hard | Hard | Easy | Hard  | hard |
| -------------------- | ---- | ---- | ---- | ---- | ----- | ---- |
control sequence
(Myers	  1979)
39

Sandwich ..  Thread ...
|     | Top (more) |     |     |     |     | Top |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- |
| A   |            |     | C   |     | A   |     | C   |
A “thread” is a portion of several
Sandwich integration
modules that together provide a
is flexible and
user-visible program feature.
| X   | Y   |     |     | Thread	  integrXation |     |     |     |
| --- | --- | --- | --- | ---------------------- | --- | --- | --- |
adaptable, but
complex to plan
Thread =	  user-­‐visible	  program	  feature across	  several	  modules
(c) 2007 Mauro Pezzè & Michal Young   Ch 21, slide 26  (c) 2007 Mauro Pezzè & Michal Young   Ch 21, slide 27
e.g.	  send	  a	  message,	  change	  user,	  create	  mailbox
Test	  each	  thread	  incrementally
Thread ...  Thread ...
+ minimize	  stubs	  and	  drivers
– integration	  plan	  may	  be	  complex
|     | Top |     |     |     |     | Top |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A   |     |     |     |     | A   |     |     |
|     | B   |     | C   |     |     | B   | C   |
Integrating one
As in sandwich
thread, then another,
integration testing, we
| X   | Y   | etc., we maximize  |     |     | X   | Y   |     |
| --- | --- | ------------------ | --- | --- | --- | --- | --- |
can minimize stubs
visibility for the user
and drivers, but the
integration 4p0lan may
be complex
(c) 2007 Mauro Pezzè & Michal Young   Ch 21, slide 28  (c) 2007 Mauro Pezzè & Michal Young   Ch 21, slide 29

Critical Modules
Test modules with highest risk first
Risk assessment is necessary first step
May include technical risks (is X feasible?),
process risks (is schedule for X realistic?),
other risks
Otherwise similar to thread or sandwich strategies
Integration testing as a risk-­‐reduction activity
deliver any bad news as early as possible
41

Program	  vs.	  System	  Testing
| Unit,	  integration  | testing                |             |            |                 |               |       |
| --------------------- | ---------------------- | ----------- | ---------- | --------------- | ------------- | ----- |
| Check	  that         | the	  code            | properly    | implements |                 | the	  design |       |
| Involves              | software	  developers |             |            |                 |               |       |
| System,	  acceptance |                        | testing     |            |                 |               |       |
| Check	  that         | the	  system          | does        | what       | the	  customer |               | wants |
| Involves              | the	  whole           | development |            | team            |               |       |
42

System	  Testing
|              |     | System        | Acceptance   | Regression     |
| ------------ | --- | ------------- | ------------ | -------------- |
| Test for ... |     | Correctness,  | Usefulness,  | Accidental     |
|              |     | completion    | satisfaction | changes        |
| Test wrt     | ... | Requirements  | User needs   | Previous tests |
specification
| Test by ...  |     | Development test  | Test group with  | Development  |
| ------------ | --- | ----------------- | ---------------- | ------------ |
|              |     | group             | users            | test group   |
|              |     | Verification      | Validation       | Verification |
43

System Testing
Comprehensive: heck the whole system
wrt. the whole specification
Based on a requirements specification of observable
behavior
Functional and non-­‐functional (performance)
Not user needs (validation)
Not opinions
Independent of design and implementation
Avoid repeating software design errors
in system test design
44

Independent V&V
f() {
...
}
The test team is independent
from the development team
avoids conflicts wrt developer's responsibility
improves objectivity, avoids bias
allows testing and coding concurrently
Can be outsourced to an independent company
45

Early Test Development
Need Product
Maintenance
Requirements definition Acceptance testing
System design System testing
Program design Integration testing
Develop system test cases early Program writing Unit testing
As part of requirements specification Code
before major design decisions have been made
Maximizes independence
Opportunity for “design for test”
Structure system for critical system testing
Agile “test first”
system test cases are the specifications
46

Global Properties
Some system properties are inherently global
Performance, latency, reliability, ...
A major focus of system testing
Find unanticipated effects, e.g., performance bottleneck
Some properties depend on the system context and use
Example: Performance depends on environment and configuration
Example: Privacy depends on system and how it is used
Example: Security depends on threat profiles
Must establish an operational envelope
Test at the edge of the envelope (check compliance with properties)
Test well beyond the envelope (check graceful degradation/failure)
47

Stress Testing
Property (e.g., performance or real-­‐time response)
parameterized by use (e.g. requests per second, size of database)
Stress testing is required
Varying parameters within the envelope, near the bounds, and beyond
Requires extensive simulation of the execution environment
Requires more resources (human and machine) than typical test cases
Separate from regular feature tests
Run less often, with more manual control
Diagnose deviations from expectation
48

Acceptance Testing
|              |     | System        | Acceptance   | Regression     |
| ------------ | --- | ------------- | ------------ | -------------- |
| Test for ... |     | Correctness,  | Usefulness,  | Accidental     |
|              |     | completion    | satisfaction | changes        |
| Test wrt     | ... | Requirements  | User needs   | Previous tests |
specification
| Test by ...  |     | Development test  | Test group with  | Development  |
| ------------ | --- | ----------------- | ---------------- | ------------ |
|              |     | group             | users            | test group   |
|              |     | Verification      | Validation       | Verification |
49

Acceptance Testing
Goal: enable the customers and users
to determine if the system meets their needs
Uncover remaining requirement discrepancies
Uncover needs unspecified in the requirements
Measuring quality, not searching for faults
Fundamentally different goal than system testing
Quantitative dependability goals
Reliability
Availability
Mean time to failure
...
50

Statistical Testing
| Quantitative	  dependability |                                |                |               | goals	  are	  statistical |        |         |
| ----------------------------- | ------------------------------ | -------------- | ------------- | --------------------------- | ------ | ------- |
| Measures                      | based                          | on	  failures |               | occuring                    | during | testing |
| Will	  this                  | be accurate                    |                | in	  typical | system	  usage?            |        |         |
| Different                     | users,	  tasks,	  experience |                |               | levels,	  …                |        |         |
Operational profile: probability distribution	  on	  inputs
| Reflecting                   | usage        |     |                   |     |         |     |
| ---------------------------- | ------------ | --- | ----------------- | --- | ------- | --- |
| Statistical                  | testing:	   |     |                   |     |         |     |
| select	  tests	  according |              |     | to	  operational |     | profile |     |
Tests	  focus	  on	  more	  used parts	  =>	  better observed reliability
Test	  reflects usage	  =>	  reliability predictions more	  accurate
| Operational |     | profiles	  are	  difficult |     |     | to	  define |     |
| ----------- | --- | ---------------------------- | --- | --- | ------------ | --- |
51

Statistical Testing Can Mislead
A small % of the operational profile may account for
a large % of failures
Example: airplane take-­‐off and landing
Example: printer
non-­‐saturated: available, no queue => print immediately (20%)
saturated: busy, queue => add to queue (79%)
transitional: busy, no queue => create queue and add to queue (1%)
probability of failures: 0.001 per test case
To have a 50% chance of detecting each fault, we must run
non saturated: 2500 test cases
saturated: 663 test cases
transitional : 50 000 test cases
Transitional likely the most complex and failure-­‐prone
52

|              |     | Regression    | Testing      |                |
| ------------ | --- | ------------- | ------------ | -------------- |
|              |     | System        | Acceptance   | Regression     |
| Test for ... |     | Correctness,  | Usefulness,  | Accidental     |
|              |     | completion    | satisfaction | changes        |
| Test wrt     | ... | Requirements  | User needs   | Previous tests |
specification
| Test by ...  |     | Development test  | Test group with  | Development  |
| ------------ | --- | ----------------- | ---------------- | ------------ |
|              |     | group             | users            | test group   |
|              |     | Verification      | Validation       | Verification |
53

Regression
Yesterday it worked, today it doesn’t
I was fixing X, and accidentally broke Y
That bug was fixed, but now it’s back
Regression = loss of correct functionality after a change
Adding new features
Changing, adapting software to new conditions
Fixing other bugs
Regression testing:
re-­‐executing tests after any change to detect regressions
Can be a major cost of software maintenance
Sometimes much more than making the change
54

Problems of Regression Test
Maintaining the test suite
After a change, which test cases must be revised,
removed, replaced or added?
Obsolete: no longer valid
⇒
should be removed
Redundant: does not differ significantly from others
⇒
may be removed or not, depending on costs
Cost of re-­‐testing
Often proportional to product size, not change size
Select or prioritize test cases
55

Selecting and Prioritizing
Regression Test Cases
Should we re-­‐run the whole test suite?
If so, in what order?
Yes, if it is cheap enough...
Test case selection: do not execute some test cases
When test cases are expensive to execute (special equipment, or
long run-­‐times, or manual intervention)
Test case prioritization: execute some test cases less often
When a very large test suite cannot be executed every day
56

Regression Test Selection
Principle:
execute only test cases related to elements that were affected by the change
Code-­‐based selection: only execute test cases that execute changed or new
code
Independent: a test case can’t find a fault in code it doesn’t execute
Variants: changed CFG nodes (control-­‐flow)
changed def-­‐use pairs (data-­‐flow)
Needs to record elements touched by each test case and modified by each
change
Specification-­‐based selection:
only execute test cases that test new and changed functionality
Not independent: a test case that is not “for” a changed feature X might find a
bug in feature X
⇒ prefer prioritization rather than selection
57

Regression Test Prioritization
Basic idea:
Execute all test cases, eventually
Execute some sooner than others
Possible priority schemes:
Specification-­‐based: priority to test cases related to changed and
added features
Round robin: Priority to least-­‐recently-­‐run test cases
Track record: Priority to test cases that have detected faults before
They probably execute code with a high fault density
Structural: Priority for executing elements that have not been
recently executed
Can be coarse-­‐grained: features, methods, files, ...
58

Summary
Test execution
Goal: Separate creative task of test design from mechanical task of
test execution
Scaffolding: drivers, stubs, harness
Oracles: comparison, self-­‐check, capture/replay
Testing activities
Unit testing: functional, structural
Integration testing: strategies
System testing: operational envelope, stress testing
Acceptance testing: statistical testing
Regression testing: selecting, prioritizing
59

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 17, 21, 22
60

Software Quality Assurance
6 – Program Analysis
Charles Pecheur
Mar 2018
1

Program Analysis
Inspection
Symbolic Execution
Program Analysis
2

Program	  Analysis
| Goal:	  find                 | faults | in	  programs |
| ----------------------------- | ------ | -------------- |
| • Run the	  code:	  testing |        |                |
But	  also
•
Examine	  the	  code: inspections
…	  and	  associated specifications,	  test	  plans,	  …
| • Analyze | the	  code:	  code	  analysis,	  proofs |       |
| --------- | ------------------------------------------- | ----- |
| manually  | or	  with                                  | tools |
3

INSPECTION
4

Inspection
Inspection:
| Systematic,	  detailed |         |               |     | review |         | of	  artifacts |
| ----------------------- | ------- | ------------- | --- | ------ | ------- | --------------- |
| to	  find              | defects | and	  assess |     |        | quality |                 |
Artifacts =	  code	  but	  also specifications,	  documentation,	  tests,	  …
Benefits
•
| Find        | and	  remove |               |     | defects |              |     |
| ----------- | ------------- | ------------- | --- | ------- | ------------ | --- |
| • Incentive |               | to	  produce |     |         | good	  code |     |
•
| Share	  coding |     |                      | norms |     | and	  practices |             |
| --------------- | --- | -------------------- | ----- | --- | ---------------- | ----------- |
| • Familiarize   |     | new	  staff	  with |       |     |                  | the	  code |
5

The Inspection Team
Team: the programmer(s) + experts
with different perspectives: junior an senior
engineers, test, managers, analysts, architects, …
4 to 6 inspectors, or less
Simple checks → one inspector
Complex checks → two inspectors
Special expertise → three or more inspectors
Moderator: external senior manager
6

Inspection	  Process
Preparation:
| Prepare                 | artifacts |             | to	  be inspected |                 |     |
| ----------------------- | --------- | ----------- | ------------------ | --------------- | --- |
| Assign                  | roles     |             |                    |                 |     |
| Gather                  | needed    | information |                    |                 |     |
| Plan	  and	  schedule |           |             | activities         | and	  meetings |     |
Review:
| Review | each | artifact,	  individually |     |     | and	  in	  teams, |
| ------ | ---- | ------------------------- | --- | --- | ------------------- |
following a	  systematic and	  consistent	  process (checklists)
Follow-­‐up:
| Notify             | developers |                             | of	  results | (reports) |     |
| ------------------ | ---------- | --------------------------- | ------------- | --------- | --- |
| Plan	  additional |            | inspections	  if	  needed |               |           |     |
7

Checklist:	  Example 1
Java  Checklist:  Level  1  inspection  (single-­pass  read-­through,  context  independent)
FEATURES  (where  to  look  and  how  to  check):
Item  (what  to  check)
FILE  HEADER:  Are  the  following items  included and  consistent? yes no comments
| Author           | and  current                                | maintainer         | identity |     |                                              |     |
| ---------------- | ------------------------------------------- | ------------------ | -------- | --- | -------------------------------------------- | --- |
| Cross-­reference |                                             | to  design  entity |          |     |                                              |     |
| Overview         | of  package  structure,  if  the  class  is |                    |          |     | the  principal  entry  point  of  a  package |     |
FILE  FOOTER:  Does it include the  following items? yes no comments
| Revision    | log  to  minimum  of  1  year |     |     | or  at  least  to |     |     |
| ----------- | ----------------------------- | --- | --- | ----------------- | --- | --- |
| most recent | point  release,  whichever    |     |     | is longer         |     |     |
IMPORT  SECTION:  Are  the  following requirements satisfied? yes no comments
Brief  comment  on  each  import  with  the  exception  of  standard  set:  java.io.*,  java.util.*
| Each imported | package  corresponds  to  a  dependence |     |     |     |     | in  the  design  documentation |
| ------------- | --------------------------------------- | --- | --- | --- | --- | ------------------------------ |
CLASS  DECLARATION:  Are  the  following  requirements  satisfied? yes no comments
The  visibility  marker  matches  the  design  document
| The  constructor  is  explicit  (if  the  class  is  not |                    |     |                  |     | static)               |     |
| -------------------------------------------------------- | ------------------ | --- | ---------------- | --- | --------------------- | --- |
| The  visibility                                          | of  the  class  is |     | consistent  with |     | the  design  document |     |
CLASS  DECLARATION  JAVADOC:  Does  the  Javadoc  header  include: yes no comments
One  sentence  summary  of  class  functionality
| Guaranteed | invariants  (for  data  structure  classes) |     |     |     |     |     |
| ---------- | ------------------------------------------- | --- | --- | --- | --- | --- |
Usage  instructions
CLASS:  Are  names compliant with the  following rules? yes no comments
| Class  or  interface:  CapitalizedWithEachInternal-­ |     |     |     |     | WordCapitalized |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --------------- | --- |
Special  case:  If  class  and  interface  have  same  base  name,  distinguish  as  ClassNameIfc  and  Class-­
NameImpl
Exception:  ClassNameEndsWithException
| Constants   |     | (final): |     |     |     |     |
| ----------- | --- | -------- | --- | --- | --- | --- |
ALL  CAPS  WITH  UNDERSCORES
| Field  name:  capsAfterFirstWord.  name |     |     |     | must  be | meaningful | outside of  context |
| --------------------------------------- | --- | --- | --- | -------- | ---------- | ------------------- |
IDIOMATIC  METHODS:  Are  names  compliant  with  the  following  rules? yes no comments
Method  name:  capsAfterFirstWord
Local  variables:  capsAfterFirstWord.
8
Name  may be short  (e.g.,  i  for  an  integer)  if  scope  of  declaration and  use  is less than 30  lines.
Factory  method  for  X:  newX

Checklist:	  Example 2
Java  Checklist:  Level  1  inspection  (single-­pass  read-­through,  context  independent)
FEATURES  (where  to  look  and  how  to  check):
Item  (what  to  check)
DATA  STRUCTURE  CLASSES:  Are  the  following requirements satisfied? yes no comments
| The  class  keeps |     | a  design  secret |     |     |     |     |     |
| ----------------- | --- | ----------------- | --- | --- | --- | --- | --- |
The  substitution  principle is respected:  Instance  of  class  can be used in  any context allowing
| instance  of  superclass |                                         |     | or  interface |                                               |          |     |     |
| ------------------------ | --------------------------------------- | --- | ------------- | --------------------------------------------- | -------- | --- | --- |
| Methods                  | are  correctly                          |     | classified    | as  constructors,  modifiers,  and  observers |          |     |     |
| There  is                | an  abstract  model  for  understanding |     |               |                                               | behavior |     |     |
The  structural  invariants  are  documented
FUNCTIONAL  (STATELESS)  CLASSES:  Are  the  following requirements satisfied? yes no comments
The  substitution  principle is respected:  Instance  of  class  can be used in  any context allowing
| instance  of  superclass |     |     | or  interface |     |     |     |     |
| ------------------------ | --- | --- | ------------- | --- | --- | --- | --- |
METHODS:  Are  the  following requirements satisfied? yes no comments
| The  method | semantics |     | are  consistent  with |     | similarly | named | methods.  For  example,  a  "put"   |
| ----------- | --------- | --- | --------------------- | --- | --------- | ----- | ----------------------------------- |
method should be semantically consistent  with "put"  methods in  standard  data  structure  libraries
| Usage  examples |     | are  provided |     | for  nontrivial | methods |     |     |
| --------------- | --- | ------------- | --- | --------------- | ------- | --- | --- |
FIELDS:  Are  the  following requirements satisfied? yes no comments
| The  field | is necessary |     | (cannot | be a  method-­local  variable) |     |     |     |
| ---------- | ------------ | --- | ------- | ------------------------------ | --- | --- | --- |
Visibility is protected or  private,  or  there is an  adequate and  documented rationale for  public
access
| Comment  describes |     |                                 | the  purpose | and  interpretation |            | of  the  field |                            |
| ------------------ | --- | ------------------------------- | ------------ | ------------------- | ---------- | -------------- | -------------------------- |
| Any constraints    |     | or  invariants  are  documented |              |                     | in  either | field          | or  class  comment  header |
DESIGN  DECISIONS:  Are  the  following requirements satisfied? yes no comments
Each design  decision is hidden in  one  class  or  a  minimum  number of  closely related and  co-­
located classes
Classes  encapsulating  a  design  decision  do  not  unnecessarily  depend  on  other  design
decisions
Adequate  usage  examples  are  provided,  particularly  of  idiomatic  sequences  of  method  calls
Design  patterns  are  used  and  referenced  where  appropriate
If  a  pattern  is  referenced:  The  code  corresponds  to  the  documented  pattern
9

Checklists
| Checklist:	  list | of	  questions	  about	  the	  artifact |     |
| ------------------ | ------------------------------------------- | --- |
Applicable	  to	  code,	  specification,	  documentation,	  tests,	  …
yes/no	  answers,	  yes =	  compliance
should be objective,	  unambiguous,	  easy to	  understand
| Different  | checklists	  at	  different              | stages |
| ---------- | ------------------------------------------ | ------ |
| level      | 1	  (simple)	  /	  level 2	  (complex) |        |
| Structured | hierarchically                             |        |
| Feature    | 1                                          |        |
Question	  1.1
Question	  1.2
| Feature | 2   |     |
| ------- | --- | --- |
Question	  2.1
…
10

Inspection:	  Effectiveness
| Experience |                              | shows	  that |             |      | code	  inspections	  are |                       |              |
| ---------- | ---------------------------- | ------------- | ----------- | ---- | -------------------------- | --------------------- | ------------ |
| very       | effective	  at	  detecting |               |             |      | faults                     |                       |              |
| Different  |                              | activities    |             | find | different                  | types	  of	  faults |              |
|            |                              |               | Preparation |      | Meeting                    |                       | Fault Found  |
Development Artifact
Discovery Activity
|                          |     |     | work per hour |     | work per hour |                     | per KLOC |
| ------------------------ | --- | --- | ------------- | --- | ------------- | ------------------- | -------- |
| Requirement Document     |     |     | 25 pages      |     | 12 pages      |                     |          |
|                          |     |     |               |     |               | Requirements review | 2.5      |
| Functional specification |     |     | 45 pages      |     | 15 pages      |                     |          |
|                          |     |     |               |     |               | Design Review       | 5.0      |
| Logic specification      |     |     | 50 pages      |     | 20 pages      | Code inspection     | 10.0     |
| Source code              |     |     | 150 LOC       |     | 75 LOC        | Integration test    | 3.0      |
| User documents           |     |     | 35 pages      |     | 20 pages      | Acceptance test     | 2.0      |
(Jones	  1991)
11

Why automated analysis
Manual program inspection
Effective in finding faults difficult to detect with testing
But humans are not good at
• repetitive and tedious tasks
• maintaining large amounts of detail
Automated analysis
Replace human inspection for some classes of faults
Support inspection by
• automating extracting and summarizing information
• navigating through relevant information
12

Static vs dynamic analysis
Static analysis: examine source code
examine the complete execution space
but may lead to false alarms
Dynamic analysis: examine execution traces
no infeasible path problem
but cannot examine the execution space
exhaustively
13

SYMBOLIC EXECUTION
14

1 { x=b;
| Symbolic	  execution: |     |     |     |     | 2 y=1;              |           |     |
| ---------------------- | --- | --- | --- | --- | ------------------- | --------- | --- |
|                        |     |     |     |     | 3  while (x>0) do { |           |     |
| Example                |     |     |     |     | 4                   | y=y*a;    |     |
|                        |     |     |     |     | 5                   | x=x-1; }  |     |
6 }
| loc | x     | y     |                   | cond	   |     | simplified	  cond	   |       |
| --- | ----- | ----- | ----------------- | -------- | --- | ---------------------- | ----- |
| 1   | ?     | ?     |                   | true     |     |                        | true  |
| 2   | B     | ?     |                   | true     |     |                        | true  |
| 3   | B     | 1     |                   | true     |     |                        | true  |
| 4   | B     | 1     |                   | B>0      |     |                        | B>0   |
| 5   | B     | 1*A   |                   | B>0      |     |                        | B>0   |
| 3   | B–1   | 1*A   |                   | B>0      |     |                        | B>0   |
| 4   | B–1   | 1*A   | B>0,B–1>0         |          |     |                        | B–1>0 |
| 5   | B–1   | 1*A*A | B>0,B–1>0         |          |     |                        | B–1>0 |
| 3   | B–1–1 | 1*A*A | B>0,B–1>0         |          |     |                        | B–1>0 |
| 6   | B–1–1 | 1*A*A | B>0,B–1>0,B–1–1≤0 |          |     |                        | B=2   |
15

Symbolic Execution
Principle: execute the program with symbolic values
Variables receive symbolic values
Execution paths accumulate symbolic conditions
Bridges program behavior to logic
Applications:
Program analysis
Test data generation
Formal verification
Tool-­‐supported!
16

Symbolic state
Values are symbolic expressions
Executing statements computes new expressions
Concrete execution Symbolic execution
low 12 low L
high 15 high H
mid -­‐ mid -­‐
mid = (high+low)/2 ; mid = (high+low)/2 ;
low 12 low L
high 15 high H
mid 13 mid (L+H)/2
17

Branching statements
char *binarySearch( char *key, char *dictKeys[ ],
char *dictValues[ ], int dictSize) {
int low = 0;
int high = dictSize - 1;
int mid;
int comparison;
Branching stmt while (high >= low) {
mid = (high + low) / 2;
comparison = strcmp( dictKeys[mid], key );
if (comparison < 0) {
low = mid + 1;
} else if ( comparison > 0 ) {
high = mid - 1;
} else {
return dictValues[mid];
}
}
return 0;
18

Executing	  branching	  statements
Both	  branches	  are	  possible	  (non-­‐determinism)
Record	  the	  condition	  for	  the	  execution	  of	  each	  branch
low	  =	  0
and high	  =	  (H-­‐1)/2	  -­‐1
and	  mid	  =	  (H-­‐1)/2
while (high >= low) {
| low	  =	  0                         |              | low	  =	  0                         |              |
| ------------------------------------- | ------------ | ------------------------------------- | ------------ |
| and	  high	  =	  (H-­‐1)/2	  -­‐1 |              | and	  high	  =	  (H-­‐1)/2	  -­‐1 |              |
| and mid	  =	  (H-­‐1)/2             |              | and mid	  =	  (H-­‐1)/2             |              |
| and (H-­‐1)/2	  -­‐                  | 1	  >=	  0 | and not	  (H-­‐1)/2	  -­‐           | 1	  >=	  0 |
19

Summary information
Path accumulate conditions
May become extremely complex
We can simplify:
replace a complex condition P
with a weaker condition W such that P => W
W describes the path with less precision
W is a summary of P
20

Example: summary information
low = L
and high = H
and mid = M
and M = (L+H)/2
simplified to
low = L
and high = H
and mid = M
and L <= M <= H
The weaker condition contains less information
21

Weaker predicates
The weaker condition contains less information
Chosen based on what must be true for correct
execution
cannot be derived automatically from source code
Weakening the predicate has a cost for testing
satisfying the predicate
does not guarantee execution along the path
22

Loops and invariants
To reason about program behavior in a loop,
we can place within the loop an invariant
while (high >= low) invariant W
{ … }
Each time program execution reaches the invariant W,
we can weaken the execution condition P to W:
• check that P => W
• substitute W for P
23

Invariant: example
char *binarySearch( char *key, char *dictKeys[ ],
char *dictValues[ ], int dictSize) {
int low = 0;
int high = dictSize -­‐ 1;
int mid;
Invariant:
int comparison;
Forall i : 0 <= i < size :
while (high >= low) {
dictKeys[i] = key =>
mid = (high + low) / 2;
low <= i <= high
comparison = strcmp( dictKeys[mid], key );
if (comparison < 0) {
low = mid + 1;
} else if ( comparison > 0 ) {
high = mid -­‐ 1;
} else {
return dictValues[mid];
}
}
24
return 0;

Pre-­‐ and post-­‐conditions
If:
• Every loop contains an invariant
• there is an assertion at the beginning of the program
• there is an assertion at the end of the program
Then:
Every possible execution path is a sequence of segments
(basic paths) from one assertion to the next
Precondition: assertion at the beginning of a segment,
Postcondition: assertion at the end of the segment
25

Verifying program correctness
The inductive invariants method (Floyd)
Verify for each basic path:
• Starting from the precondition,
• Executing the program segment,
• The postcondition holds at the end.
Then the execution of any path is correct
26

Program Proof: Example
start 0 <= lo
for (i = lo; i <= hi; i = i + 1) {
hi < length(a)
if (a[i] == e) return true;
}
i = lo
return false;
i >= lo
loop ∀j : lo ≤ j ≤ i – 1 : a[j] ≠ e
false
i <= hi result = false
true
true
a[i] == e result = true
false
i = i + 1
result <-­‐> ∃j : lo ≤ j ≤ hi : a[j] == e
end
27

Program	  Proof:	  Basic	  Paths
start
i	  =	  lo
loop loop
| loop | loop |     |     |
| ---- | ---- | --- | --- |
false
| i	  <=	  hi |     | i	  <=	  hi | result =	  false |
| ------------- | --- | ------------- | ----------------- |
i	  <=	  hi
| true | true |     |     |
| ---- | ---- | --- | --- |
true
| a[i]	  ==	  e | a[i]	  ==	  e | result =	  true |     |
| --------------- | --------------- | ---------------- | --- |
false
i	  =	  i	  +	  1
end
end
28

| Symbolic |     |     | Execution:	  Example |     |     |     |     |
| -------- | --- | --- | --------------------- | --- | --- | --- | --- |
loop
|               | i =	  i |     | ∀j :	  lo | ≤	  j ≤	  i | – 1	  :	  a[j]	  ≠	  e                  |          |     |
| ------------- | -------- | --- | ---------- | ------------- | ------------------------------------------- | -------- | --- |
|               |          | 0   |            |               | 0	                                         |          |     |
| i	  <=	  hi |          |     |            | exec          |                                             |          |     |
| true          | i =	  i |     | ∀j :	  lo | ≤	  j        | ≤	  i – 1	  :	  a[j]	  ≠	  e,	  	  i | <=	  hi |     |
|               |          | 0   |            |               | 0                                           | 0        |     |
exec
a[i]	  ==	  e
∀j
false i =	  i :	  lo ≤	  j ≤	  i – 1	  :	  a[j]	  ≠	  e,	  	  i <=	  hi,	  	  a[i ]	  ≠	  e
|     |     | 0   |     |     | 0   | 0   | 0   |
| --- | --- | --- | --- | --- | --- | --- | --- |
exec
i	  =	  i	  +	  1
∀j
|     | i =	  i | +	  1 | :	  lo | ≤	  j | ≤	  i – 1	  :	  a[j]	  ≠	  e,	  	  i | <=	  hi,	  	  a[i | ]	  ≠	  e |
| --- | -------- | ------ | ------- | ------ | ------------------------------------------- | -------------------- | ----------- |
|     |          | 0      |         |        | 0                                           | 0                    | 0           |
⇒
loop
∀j
|     |     | :	  lo ≤	  j | ≤	  i – | 1	  :	  a[j]	  ≠	  e |     |     |     |
| --- | --- | -------------- | -------- | ------------------------ | --- | --- | --- |
29

Compositional reasoning
Follow the hierarchical structure of a program
at a small scale (within a single procedure)
at larger scales (across multiple procedures…)
Hoare triple: [pre] block [post]
If pre is satisfied at the entry to the block,
Then post is satisfied after execution of the block.
30

Compositional	  reasoning
Summarize	  the	  effect	  of	  a	  block	  of	  program	  by	  a	  contract
| [pre]	  block | [post]        |                       |
| -------------- | ------------- | --------------------- |
| Prove          | that	  block | satisfies	  pre/post |
Then	  use	  the	  contract	  wherever	  the	  block	  is	  used
In	  particular,	  for	  procedures/methods/routines
Example:	  binarySearch
| [	  forall | i,j :	  0	  <=	  i | <	  j	  <	  size	  :	  keys[i]	  <=	  keys[j]	  ] |
| ----------- | --------------------- | --------------------------------------------------------- |
s	  =	  binarySearch(k,	  keys,	  vals,	  size)
[	  (s	  =	  v	  and	  exists	  i :	  0	  ≤ i <	  size	  :	  keys[i]	  =	  k	  and	  vals[i]	  =	  v)
or	  (s	  =	  0	  and	  not	  exists	  i :	  0	  <=	  i <	  size	  :	  keys[i]	  =	  k)	  ]
31

Data structures and classes
Data structure module (class) =
data (encapsulated) + operations =
variables + procedures (methods)
The specifications of methods are strongly interrelated
Contract:
• abstraction function abs
relates data structure D to an abstract model abs(D)
e.g. abs : Dictionary → {<key, value>}
• structural invariant ok
data structure characteristics that must be maintained
e.g. ok : Dictionary → bool
32

Data structure : example
Dictionary structure
abs : Dictionary → {<key, value>}
ok : Dictionary → bool
Contract for Dictionary.get:
[<k,v> in abs(dict) and ok(dict) ]
o = dict.get(k)
[ o = v and ok(dict) ]
33

| Symbolic                 |               | execution:	  other |          |     |           |          |     | domains |
| ------------------------ | ------------- | ------------------- | -------- | --- | --------- | -------- | --- | ------- |
| So	  far:	  fully      | precise       |                     | symbolic |     | values    |          |     |         |
| + allows                 | proofs        |                     |          |     |           |          |     |         |
| – complicated,	  proofs |               |                     |          | may | not	  be | workable |     |         |
| Wider                    | applications: |                     |          |     |           |          |     |         |
• limited symbolic information	  rather than full	  symbolic
value
| e.g.	  {	  unassigned,	  assigned |         |        |        |     | }    |       |             |     |
| ------------------------------------ | ------- | ------ | ------ | --- | ---- | ----- | ----------- | --- |
| • find                               | limited | faults | rather |     | than | prove | correctness |     |
e.g.	  uninitialized variables,	  memory	  leaks,	  null pointers,	  SQL
injections,	  buffer	  overflow
•
| trade | accuracy |     | for	  efficiency |     |     |     |     |     |
| ----- | -------- | --- | ----------------- | --- | --- | --- | --- | --- |
34

PROGRAM ANALYSIS
35

Symbolic Testing
Abstract variables with few symbolic values
Apply symbolic execution
No need to follow all paths
explore paths to a limited depth
prune exploration by some criterion
Example: analysis of pointer misuse
Pointer variables: { null, notnull, invalid, unknown }
Other variables represented by constraints
36

Symbolic testing: sensitivity
Symbolic testing is path sensitive
Different symbolic states from different paths
to the same location
Symbolic testing is partly context sensitive
Different symbolic states from different call sequences
This is a strength of symbolic checking
detailed description of how a fault is reached
also very costly
reduce costs by memoizing entry and exit conditions
37

Summarizing Execution Paths
Find all program faults of a certain kind
do not prune exploration of paths (symbolic testing)
abstract enough to fold the state space down to a
size that can be exhaustively explored
Example: pointer analysis
Accuracy / efficiency compromise:
merge different paths to same state or not
merge different contexts to same state or not
38

Pointer Analysis
Every pointer variable represented by a machine with three states:
deallocate
deallocate
maybe not
invalid
null null
allocate
initialize
Conditional branches may trigger transitions
E.g., testing for non-­‐null : maybe null → not null
Errors:
Deallocation in maybe null
Dereference in maybe null
Dereference in invalid
39

Example: Buffer Overflow
…
int main (int argc, char *argv[]) {
char sentinel_pre[] = "2B2B2B2B2B";
char subject[] = "AndPlus+%26%2B+%0D%";
char sentinel_post[] = "26262626";
Output parameter
char *outbuf = (char *) malloc(10);
int return_code;
of fixed length
printf("First test, subject into outbuf\n"); Can overrun the
return_code = cgi_decode(subject, outbuf);
output buffer
printf("Original: %s\n", subject);
printf("Decoded: %s\n", outbuf);
printf("Return code: %d\n", return_code);
printf("Second test, argv[1] into outbuf\n");
printf("Argc is %d\n", argc);
assert(argc == 2);
return_code = cgi_decode(argv[1], outbuf);
printf("Original: %s\n", argv[1]);
printf("Decoded: %s\n", outbuf);
printf("Return code: %d\n", return_code);
}…
40

Dynamic Memory Analysis (with
Purify)
[I] Starting main
[E] ABR: Array bounds read in printf {1 occurrence}
Reading 11 bytes from 0x00e74af8 (1 byte at 0x00e74b02 illegal)
Address 0x00e74af8 is at the beginning of a 10 byte block
Address 0x00e74af8 points to a malloc'd block in heap 0x00e70000
Thread ID: 0xd64
...
[E] ABR: Array bounds read in printf {1 occurrence}
Reading 11 bytes from 0x00e74af8 (1 byte at 0x00e74b02 illegal)
Address 0x00e74af8 is at the beginning of a 10 byte block
Address 0x00e74af8 points to a malloc'd block in heap 0x00e70000
Thread ID: 0xd64
...
[E] ABWL: Late detect array bounds write {1 occurrence}
Memory corruption detected, 14 bytes at 0x00e74b02
Address 0x00e74b02 is 1 byte past the end of a 10 byte block at 0x00e74af8
Address 0x00e74b02 points to a malloc'd block in heap 0x00e70000
63 memory operations and 3 seconds since last-known good heap state
Detection location - error occurred before the following function call
printf [MSVCRT.dll]
...
Allocation location Identifies
malloc [MSVCRT.dll]
... the problem
[I] Summary of all memory leaks... {482 bytes, 5 blocks}
...
[I] Exiting with code 0 (0x00000000)
Process time: 50 milliseconds
[I] Program terminated ...
41

Memory Analysis
Dynamic analysis: track program execution
Instrument progMraemm too rtrya cAen maelymsoisr y access Data Races
Record the state of each memory location
•! Instrument program to trace memory access
•! Testing: not effective
Detect accesses incompatible with the current state
–! record the state of each memory location
(nondeterministic interleaving of threads)
–! detect accesses incompatible with the current state
access unallocated memory
•! attempts to access unallocated memory
read from uninitialized memory •! Static analysis:
•! read from uninitialized memory locations
arr–a! ya rbraoy ubnoudnsd sv viioollaattioionsn: s (unallocated locations before and after computationally expensive, and approximated
each a•!rardady m)emory locations with state unallocated before and after each array
•! Dynamic analysis:
•! attempts to access these locations are detected immediately
can amplify sensitivity of testing to detect
Unallocated
allocate potential data races
(unwritable and unreadable)
deallocate
–! avoid pessimistic inaccuracy of finite state verification
Allocated and uninitialized Allocated and initialized
deallocate –! Reduce optimistic inaccuracy of testing
(writable, but unreadable) (readable and writable)
initialize
42
(c) 2007 Mauro Pezzè & Michal Young Ch 19, slide 17 (c) 2007 Mauro Pezzè & Michal Young Ch 19, slide 18
Simple lockset analysis: example
Dynamic Lockset Analysis
Thread Program trace Locks held Lockset(x)
•! Lockset discipline: set of rules to prevent data races
{} {lck1, lck2} INIT:all locks for x
–! Every variable shared between threads must be protected by a
thread A lock(lck1)
mutual exclusion lock
{lck1} lck1 held
–! ….
x=x+1
•! Dynamic lockset analysis detects violation of the locking
{lck1} Intersect with
discipline locks held
unlock(lck1}
–! Identify set of mutual exclusion locks held by threads when
{}
accessing each shared variable
tread B lock{lck2}
–! INIT: each shared variable is associated with all available locks
{lck2}
–! RUN: thread accesses a shared variable
x=x+1 lck2 held
•! intersect current set of candidate locks with locks held by the thread
–! END: set of locks after executing a test = set of locks always held {}
by threads accessing that variable unlock(lck2} Empty intersection
potential
•! empty set for v = no lock consistently protects v
{}
race
(c) 2007 Mauro Pezzè & Michal Young Ch 19, slide 19 (c) 2007 Mauro Pezzè & Michal Young Ch 19, slide 20

Data Races
Data race:
two threads access a location, and
at least one is a write, and
there is no lock protecting that location
Testing: not effective
nondeterministic interleaving of threads
Static analysis: expensive, and approximated
Dynamic analysis: amplify sensitivity of testing to
detect potential data races
43

Dynamic Lockset Analysis
Lockset discipline:
Every shared variable must be protected by a
lock
Dynamic lockset analysis:
detects violation of the locking discipline
44

Lockset Analysis: algorithm
Identify set of locks held by threads when accessing each
shared variable
For each variable x, a set Lockset(x)
INIT: Lockset(x) = {all locks}
thread A accesses x: Lockset(x) = Lockset(x) ∩ Locks(A)
END: if Lockset(x) = {} report ERROR
no lock consistently protects v
45

Simple lockset analysis: example
Thread Program trace Locks held Lockset(x)
{} {lck1, lck2} INIT:all locks for x
thread A lock(lck1)
lck1 held
{lck1}
x=x+1
Intersect with
{lck1}
locks held
unlock(lck1}
{}
tread B lock{lck2}
{lck2}
lck2 held
x=x+1
{} Empty intersection
potential
unlock(lck2}
race
{}
46

Lockset	  with	  multiple	  reads
Handling Realistic Cases  Extracting Models from Execution
simple	  locking	  discipline	  violated	  by
•! simple locking discipline violated by   •! Executions reveals information about a program
initialization	  of	  shared	  variables	  without	  holding	  a	  lock
–! initialization of shared variables without holding a lock
writing	  shared	  variables	  during	  initialization	  without	  locks
•! Analysis
–! writing shared variables during initialization without locks
allowing	  multiple	  readers	  in	  mutual	  exclusion	  with	  single	  writers
–! gather information from execution
–! allowing multiple readers in mutual exclusion with single writers
–! synthesize models that characterize those executions
Delay analysis
| Virgin |     | till after initialization  |     |
| ------ | --- | -------------------------- | --- |
(second thread)
write
Multiple writers
report violations
| Exclusive |     | write/new thread |     |
| --------- | --- | ---------------- | --- |
read/write/first thread
Shared-Modified
read/new thread
read
Multiple readers
| Shared |     | write |     |
| ------ | --- | ----- | --- |
single writer
do not report violations
47
(c) 2007 Mauro Pezzè & Michal Young   Ch 19, slide 21  (c) 2007 Mauro Pezzè & Michal Young   Ch 19, slide 22
Example: AVL tree
Automatically Extracting Models
private AvlNode insert( Comparable x, AvlNode t ){
  if( t == null )  •! Start with a set of predicates
|     | t = new AvlNode( x, null, null );  |     |     |
| --- | ---------------------------------- | --- | --- |
  else if( x.compareTo( t.element ) < 0 ){  –! generated from templates
|     | t.left = insert( x, t.left );  |     |     |
| --- | ------------------------------ | --- | --- |
    if( height( t.left ) - height( t.right ) == 2 )  –! instantiated on program variables
|     |     | if( x.compareTo( t.left.element ) < 0 )  |     |
| --- | --- | ---------------------------------------- | --- |
–! at given execution points
|     |     |       | t = rotateWithLeftChild( t );  |
| --- | --- | ----- | ------------------------------ |
|     |     | else  |                                |
•! Refine the set by eliminating predicates
|     |     |     | t = doubleWithLeftChild( t );              |
| --- | --- | --- | ------------------------------------------ |
Behavior model
  }else if( x.compareTo( t.element ) > 0 ){
at the end of   violated during execution
|     | t.right = insert( x, t.right );  |     |     |
| --- | -------------------------------- | --- | --- |
insert:
|     | if( height( t.right ) - height( t.left ) == 2 )  |                                           |     |
| --- | ------------------------------------------------ | ----------------------------------------- | --- |
|     |                                                  | if( x.compareTo( t.right.element ) > 0 )  |     |
father > left
|     |     |     | t = rotateWithRightChild( t );  |
| --- | --- | --- | ------------------------------- |
father < right
|     |     | else  |     |
| --- | --- | ----- | --- |
diffHeight one of
|     |     |     | t = doubleWithRightChild( t );  |
| --- | --- | --- | ------------------------------- |
     {-1,0,1}
  } else
|     | ;  // Duplicate; do nothing  |     |     |
| --- | ---------------------------- | --- | --- |
  t.height = max( height( t.left ), height( t.right ) ) + 1;
  return t;
}
(c) 2007 Mauro Pezzè & Michal Young   Ch 19, slide 23  (c) 2007 Mauro Pezzè & Michal Young   Ch 19, slide 24

Summary
Inspection
Teams, checklists
Symbolic execution
symbolic values, constraints on paths
program proofs, compositional reasoning, contracts
other domains, FSM
Program analysis
Symbolic testing: partial symbolic execution
Memory analysis: dynamic
Lockset analysis: dynamic
Balance exhaustiveness, precision, and cost
path-­‐sensitive or insensitive, context-­‐sensitive or insensitive
48

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 7, 18, 19
49

Software Quality Assurance
7 – Finite State Analysis
Charles Pecheur
Apr 2018
1

Contents
Finite state verification
Intensional models
Model refinement
Data model verification
2

FINITE STATE VERIFICATION
3

Finite state verification
Properties to
be proved
symbolic execution
complex
and formal reasoning
finite state
verification
control
and data flow
models
simple
Computational
cost
low high
4

Finite state verification
Finite state verification:
prove some significant properties
on a finite model of the infinite execution space
a.k.a. Model Checking
Techniques from symbolic execution and formal verification
Finite models of the potentially infinite state space
Balance trade-­‐offs among
generality of properties to be checked
class of programs or models that can be checked
computational effort in checking
human effort in producing models and specifying properties
Most important properties of program execution are undecidable in general
5

Cost trade-­‐offs
Human effort and skill are required
to prepare a finite state model
to prepare a suitable specification for automated
analysis
Computational cost of verification
model and specification must be tuned to
make verification feasible
⇒
impacts the human effort and skill
less expensive if analysis is fast
6

Iterative process
Prepare a model and specification
Repeat:
Attempt verification
Receive reports of impossible or unimportant faults
Refine the specification and/or the model
Until no impossible or unimportant faults
7

Analysis of models
Analysis of models
Cost trade-offs
...
public static Table 1
getTable 1() {
if (ref == null ) {
• Human effort and skill are required synchronized (Table 1) {
if (ref == null ){
ref = new Table 1(); No concurrent
– to prepare a finite state model ref.initialize (); modifications of
} Table1
}
– to prepare a suitable specification for automated analysis }
return ref ;
}...
• Iterative process:
Direct check of source /design
PROGRAM or DESIGN PROPERTY OF INTEREST
(impractical or impossible )
– prepare a model and specify properties
– attempt verification
Derive models
of software Implication
– receive reports of impossible or unimportant faults
or design
– refine the specification or the model
• Automated step Algorithmic check
MODEL PROPERTY OF THE MODEL
of the model for the property
– computationally costly (a) (x)
• computational cost impacts the cost of preparing model and (b) (y)
specification, which must be tuned to make verification feasible (c) never(<d>and <y>)
(d)
– manually refining model and specification less expensive with
(e)
near-interactive analysis tools
(f)
8
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 5 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 6
Defining the global state space –
Applications for Finite State Verification
Concurrent system example
• Concurrent (multi-threaded, distributed, ...) • Deriving a good finite state model is hard
– Difficult to test thoroughly (apparent non- • Example: finite state machine model of a
determinism based on scheduler); sensitive to
program with multiple threads of control
differences between development environment and
– Simplifying assumptions
field environment
• we can determine in advance the number of threads
– First and most well-developed application of FSV
• we can obtain a finite state machine model of each thread
• Data models
• we can identify the points at which processes can interact
– Difficult to identify “corner cases” and interactions – State of the whole system model
among constraints, or to thoroughly test them = tuple of states of individual process models
• Security – Transition = transition of one or more of the
individual processes, acting individually or in concert
– Some threats depend on unusual (and untested) use
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 7 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 8

Applications for
Finite State Verification
Concurrent (multi-­‐threaded, distributed, ...)
Difficult to test thoroughly (scheduler)
Sensitive to environment differences
First and most well-­‐developed application of FSV
Data models
Identify “corner cases” and interactions among
constraints
Security
Some threats depend on unusual (and untested) use
9

Model	  and	  property
| The	  finite | state	  model |                              |     |     |     |         |            |
| ------------- | -------------- | ---------------------------- | --- | --- | --- | ------- | ---------- |
| Derived       | from           | the	  program	  or	  from |     |     |     | another | source	   |
(specification)
| Or	  program	  derived |     |     |     | from | model |     |     |
| ------------------------ | --- | --- | --- | ---- | ----- | --- | --- |
⇔
| Consistency |     | program	   |     |     | model |     |     |
| ----------- | --- | ----------- | --- | --- | ----- | --- | --- |
The	  property
| General,	  implicit             |                |     | (deadlock,	  null |                      |           | pointers,	  …) |     |
| -------------------------------- | -------------- | --- | ------------------ | -------------------- | --------- | --------------- | --- |
| Or	  explicit,	  specification |                |     |                    |                      | formalism | (logic)         |     |
| May	  need                      | to	  simplify |     |                    | (over-­‐approximate) |           |                 |     |
10

The model: concurrent system
Finite state machine model
of a program with multiple threads
Simplifying assumptions
determined number of threads
finite state model of each thread
identified interaction points between threads
State
= tuple of states of individual thread models
Transition
= local transition of one individual thread
or joint transition of several interacting threads
11

Example: in-­‐memory table
Specification:
In-­‐memory data structure
Initialized at system start-­‐up from configuration
Initialization of the data structure must appear atomic
The system must be reinitialized on occasion
The structure is kept in memory
Implementation (with bugs):
No lock unless needed (Java synchronized): too expensive (!?)
Double-­‐checked locking idiom for a fast system (!?)
(Bad decisions... but extremely hard to find the bug through
testing)
12

In-­‐memory	  table:	  implementation
| class | Table1 { |     |     |     | public void |     | reinit()  |     |
| ----- | -------- | --- | --- | --- | ----------- | --- | --------- | --- |
{ needsInit = true; }
|     | private static       |     | Table1 ref | = null;  |                      |     |     |      |
| --- | -------------------- | --- | ---------- | -------- | -------------------- | --- | --- | ---- |
|     | private boolean      |     | needsInit  | = true;  |                      |     |     |      |
|     |                      |     |            |          | private synchronized |     |     | void |
|     | private ElementClass |     | [ ]        |          |                      |     |     |      |
initialize() {
| theValues; |                      |     |     |     | . . .  |           |          |     |
| ---------- | -------------------- | --- | --- | --- | ------ | --------- | -------- | --- |
|            | private Table1() { } |     |     |     |        | needsInit | = false; |     |
}
| public static |         | Table1 getTable1() { |     |     |            |     |            |      |
| ------------- | ------- | -------------------- | --- | --- | ---------- | --- | ---------- | ---- |
|               |         |                      |     |     | public int |     | lookup(int | i) { |
|               | if (ref | == null)             |     |     |            |     |            |      |
if (needsInit) {
|     | { synchedInitialize(); } |     |     |     |     | synchronized(this) { |               |     |
| --- | ------------------------ | --- | --- | --- | --- | -------------------- | ------------- | --- |
|     |                          |     |     |     |     | if                   | (needsInit) { |     |
|     | return ref;              |     |     |     |     |                      |               |     |
this.initialize();
}
}
}
WRONG!
| private static        |         | synchronized |     | void |     | }                       |                      |     |
| --------------------- | ------- | ------------ | --- | ---- | --- | ----------------------- | -------------------- | --- |
| synchedInitialize() { |         |              |     |      |     | return                  | theValues[i].getX()  |     |
|                       | if (ref | == null) {   |     |      |     | + theValues[i].getY();  |                      |     |
}
|     | ref | = new Table1();  |     |     |     |     |     |     |
| --- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
. . .
ref.initialize();
}
}
double-­‐checked locking:
}
|     |     |     |     |     |     | only acquire | the	  lock	  if	  ref | ==	  null |
| --- | --- | --- | --- | --- | --- | ------------ | ------------------------ | ---------- |
|     |     |     |     |     |     | only works   | for	  initialization!   |            |
13

Concurrent system example –
State space exploration –
implementation
Concurrent system example
class Table1 { public void reinit()
{ needsInit = true; }
private static Table1 ref = null;
private boolean needsInit = true;
• Specification: an on-line purchasing system
private synchronized void
private ElementClass [ ]
initialize() {
theValues;
. . .
– In-memory data structure initialized by reading
private Table1() { }
needsInit = false;
configuration tables at system start-up }
public static Table1 getTable1() {
public int lookup(int i) {
– Initialization of the data structure must appear atomic
if (ref == null)
if (needsInit) {
{ synchedInitialize(); }
synchronized(this) {
– The system must be reinitialized on occasion
return ref; if (needsInit) {
this.initialize();
}
– The structure is kept in memory
}
}
private static synchronized void
• Implementation (with bugs): }
synchedInitialize() {
return theValues[i].getX()
if (ref == null) { + theValues[i].getY();
– No monitor (Java synchronized): too expensive*
}
ref = new Table1();
. . .
ref.initialize();
– Double-checked locking idiom* for a fast system }
}
}
*Bad decision, broken idiom ... but extremely hard to find the
bug through testing.
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 9 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 10
In-­‐memory table: thread model
A finite state machine model for each thread
Analysis
(a) (x)
• Start from models of individual threads
lookup() reinit()
needsInit==true needsInit=true
• Systematically trace all the possible
(b) (y)
interleavings of threads
obtain lock
E
• Like hand-executing all possible sequences of execution,
(c)
but automated
needsInit==true
needsInit==false
(d)
needsInit==false modifying
needsInit=false
... begin by constructing a finite state machine
(e)
model of each individual thread
... release lock
(f)
reading
14
E
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 11 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 12

In-­‐memory table: analysis
Start from models of N individual threads
Systematically trace all the possible
interleavings
with Java lock access rules
Doing this by hand is completely impractical
15

SPIN
SPIN:	  one	  of	   the	  most famous traditional model
checkers
| Developed | at	  Bell	  Labs |     | (G.	  Holzmann) |     |     |     |
| --------- | ------------------ | --- | ---------------- | --- | --- | --- |
see http://spinroot.com
| Promela:	  modelling                           |     | language |     | of	  SPIN |         |          |
| ----------------------------------------------- | --- | -------- | --- | ---------- | ------- | -------- |
| simple	  imperative                            |     | language |     | with       | guarded | commands |
| Properties:	  assertions,	  temporal	  logic |     |          |     |            |         | (LTL)    |
Efficient	  implementation
| Numerous | optimization |     | options	  and	  other |     |     | features |
| -------- | ------------ | --- | ----------------------- | --- | --- | -------- |
16

|     | SPIN:	  Promela |     |     | example |     |
| --- | ---------------- | --- | --- | ------- | --- |
mtype =	  {	  msg0,	  msg1,	  ack0,	  ack1	  }; pecheur@delvaux:~/spin>	  spin	  -­‐a	  abp
chan sender	  =	  [1]	  of	  {	  mtype }; pecheur@delvaux:~/spin>	  gcc -­‐o	  pan	  pan.c
| chan receiver	  =	  [1]	  of	  {	  mtype |     | };  | pecheur@delvaux:~/spin>	  ./pan |     |     |
| --------------------------------------------- | --- | --- | -------------------------------- | --- | --- |
hint:	  this	  search	  is	  more	  efficient	  if	  pan.c is	  compiled	  -­‐DSAFETY
inline	  phase(msg,	  good_ack,	  bad_ack) (Spin	  Version	  4.2.7	  -­‐-­‐ 23	  June	  2006)
| {   |     |     | +	  Partial	  Order	  Reduction |     |     |
| --- | --- | --- | ---------------------------------- | --- | --- |
do
| ::	  sender?good_ack |     | -­‐>	  break | Full	  statespace | search	  for: |     |
| --------------------- | --- | ------------- | ------------------ | -------------- | --- |
::	  sender?bad_ack never	  claim	  	  	  	  	  	  	  	  	  	  	  	  	  -­‐ (none	  specified)
| ::	  timeout	  -­‐>	   |                     |     | assertion	  violations	  	  	  	  +            |     |                   |
| ------------------------- | ------------------- | --- | --------------------------------------------------- | --- | ----------------- |
|                           | if                  |     | acceptance	  	  	  cycles	  	  	  	  	  -­‐ |     | (not	  selected) |
|                           | ::	  receiver!msg; |     | invalid	  end	  states	  	  	  	  	  	  +   |     |                   |
::	  skip	  /*	  lose	  message	  */
fi; State-­‐vector	  28	  byte,	  depth	  reached	  9,	  errors:	  0
| od  |     |     | 12	  states,	  stored |     |     |
| --- | --- | --- | ----------------------- | --- | --- |
| }   |     |     | 3	  states,	  matched |     |     |
15	  transitions	  (=	  stored+matched)
| /*	  ...	  */ |     |     | 0	  atomic	  steps |     |     |
| --------------- | --- | --- | -------------------- | --- | --- |
hash	  conflicts:	  0	  (resolved)
2.622	  	  	  memory	  usage	  (Mbyte)
17

In-­‐memory	  table	  in	  Promela
...
| bool	  needsInit     | =	  true, | proctype                            | Lookup(int | id	  )	  { |
| --------------------- | ---------- | ----------------------------------- | ---------- | ------------ |
| locked	  =	  false, |            | if	  ::	  (needsInit)	  -­‐>	   |            |              |
modifying =	  false; atomic	  {	  !	  locked	  	  -­‐>	  locked	  =	  true;	  };
needsinit==true
if	  	  ::	  (needsInit)	  -­‐>
proctype reInit()	  { assert	  (!	  modifying);	   write/write race
| needsInit | =	  true; | modifying	  =	  true;	  	   |     |     |
| --------- | ---------- | ------------------------------- | --- | --- |
acquire lock
| }   |     | /*	  	  Initialization	  happens	  here	  */ |     |     |
| --- | --- | ------------------------------------------------- | --- | --- |
modifying	  =	  false	  ;
| init { |     | needsInit | =	  false; |     |
| ------ | --- | --------- | ----------- | --- |
...
| run	  reInit();  |     | ::	  (!	  needsInit)	  -­‐>	   |     |     |
| ----------------- | --- | ---------------------------------- | --- | --- |
| run	  Lookup(1); |     | skip;	                            |     |     |
| run	  Lookup(2); |     | fi;                                |     |     |
| }                 |     | locked	  =	  false	  ;          |     |     |
fi;
read/write race
assert	  	  (!	  modifying);}
/*	  return	  a	  value	  from	  lookup()	  */
}
18

In-­‐memory table: run Spin
Depth=10 States=51 Transitions=92 Memory=2.302
pan: assertion violated !(modifying) (at depth 17)
pan: wrote pan_in.trail
(Spin Version 4.2.5 -- 2 April 2005)
…
0.16 real 0.00 user 0.03 sys
19

In-­‐memory table: Spin trace
Starting reInit with pid 1
1: proc 0 (:init::1) doublecheck.spin:32 (state 1) [(run reInit())]
Starting Lookup with pid 2
2: proc 0 (:init::1) doublecheck.spin:33 (state 2) [(run Lookup(1))]
Starting Lookup with pid 3
3: proc 0 (:init::1) doublecheck.spin:34 (state 3) [(run Lookup(2))]
4: proc 3 (Lookup:1) doublecheck.spin:6 (state 1) [(needsInit)]
5: proc 3 (Lookup:1) doublecheck.spin:8 (state 2) [(!(locked))]
5: proc 3 (Lookup:1) doublecheck.spin:8 (state 3) [locked = 1]
6: proc 3 (Lookup:1) doublecheck.spin:10 (state 5) [(needsInit)]
7: proc 3 (Lookup:1) doublecheck.spin:12 (state 6) [assert(!(modifying))]
8: proc 3 (Lookup:1) doublecheck.spin:13 (state 7) [modifying = 1]
9: proc 3 (Lookup:1) doublecheck.spin:15 (state 8) [modifying = 0]
10: proc 3 (Lookup:1) doublecheck.spin:16 (state 9) [needsInit = 0]
11: proc 3 (Lookup:1) doublecheck.spin:21 (state 14) [locked = 0]
12: proc 1 (reInit:1) doublecheck.spin:28 (state 1) [needsInit = 1]
13: proc 2 (Lookup:1) doublecheck.spin:6 (state 1) [(needsInit)]
14: proc 2 (Lookup:1) doublecheck.spin:8 (state 2) [(!(locked))]
14: proc 2 (Lookup:1) doublecheck.spin:8 (state 3) [locked = 1]
15: proc 2 (Lookup:1) doublecheck.spin:10 (state 5) [(needsInit)]
16: proc 2 (Lookup:1) doublecheck.spin:12 (state 6) [assert(!(modifying))]
17: proc 2 (Lookup:1) doublecheck.spin:13 (state 7) [modifying = 1]
spin: doublecheck.spin:24, Error: assertion violated
spin: text of failed assertion: assert(!(modifying))
18: proc 3 (Lookup:1) doublecheck.spin:24 (state 17) [assert(!(modifying))]
20

Express the model in Promela
Analysis
...
proctype Lookup(int id ) {
• Java threading rules: if :: (needsInit) ->
atomic { ! locked -> locked = true; };
– when one thread has obtained a monitor lock
needsinit==true if :: (needsInit) ->
assert (! modifying);
– the other thread cannot obtain the same lock
modifying = true;
• Locking
acquire lock /* Initialization happens here */
modifying = false ;
– prevents threads from concurrently calling initialize
needsInit = false;
– Does not prevent possible race condition between
... :: (! needsInit) ->
threads executing the lookup method
skip;
fi;
• Tracing possible executions by hand is
locked = false ;
completely impractical
fi;
assert (! modifying);}
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 13 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 14
In-­‐memory table: program trace
Run Spin; Inspect Output Interpret the trace
proc 3 (lookup) proc 1 (reinit) proc 2 (lookup)
Spin
• Depth-first search of possible executions of the model (a) public init lookup (int i)
(b) if (needsInit ) {
• Explores 10 states and 51 state transitions in 0.16 seconds synchronized (this) {
(c)
if (needsInit ) {
(d)
• Finds a sequence of 17 transitions from the initial state of the
this.initialize();
(e)
}
model to a state in which one of the assertions in the model
}
evaluates to false
}
Depth=10 States=51 Transitions=92 Memory=2.302
(x) public void reinit ()
pan: assertion violated !(modifying) (at depth 17) { needsInit = true; }
(y)
pan: wrote pan_in.trail
(Spin Version 4.2.5 -- 2 April 2005)
(a) public init lookup (int i)
… … (b) if (needsInit ) {
return (c) synchronized (this) {
0.16 real 0.00 user 0.03 sys (f) theValues [i].getX() (d) if (needsInit ) {
Read/write
+ theValues [i].getY(); this.initialize();
Race condition
} ...
States (f) and (d)
21
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 15 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 16

Safety	  properties
| Safety:	  	  bad |     |     | things | should | not | happen |     |     |
| ------------------ | --- | --- | ------ | ------ | --- | ------ | --- | --- |
Examples:
•
|     | invariant |     | violation,	  assertion |     |     | violation |     |     |
| --- | --------- | --- | ----------------------- | --- | --- | --------- | --- | --- |
•
|     | mutual |               | exclusion:	  two |     | processes   |       | should | not |
| --- | ------ | ------------- | ----------------- | --- | ----------- | ----- | ------ | --- |
|     | modify | a	  variable |                   | at  | the	  same | time. |        |     |
•
|         | [P]	  S                    | [Q]	  :	  partial |     | correctness |        |     |     |     |
| ------- | --------------------------- | ------------------- | --- | ----------- | ------ | --- | --- | --- |
| Specify | with	  assert(	  ...	  ) |                     |     |             |        |     |     |     |
| Verify  | with	  reachability        |                     |     |             | (easy) |     |     |     |
22

Liveness properties
| Liveness:	  	  good |     | things | should | eventually | happen |     |
| --------------------- | --- | ------ | ------ | ---------- | ------ | --- |
Examples:
• response:	  if I	  push the	  button,	  eventually the
|         | elevator	  should            |         | arrive  |              |     |           |
| ------- | ----------------------------- | ------- | ------- | ------------ | --- | --------- |
| •       | fairness:	  all              | enabled | threads | get executed |     |           |
| •       | program termination           |         |         |              |     |           |
| Specify | in	  temporal                |         | logic   |              |     |           |
| Verify  | with	  automata,	  repeated |         |         | reachability |     | (more	   |
expensive)
23

|     |     |     |     | LTL: |     | Principle |     |     |     |
| --- | --- | --- | --- | ---- | --- | --------- | --- | --- | --- |
Temporal	  logic:	  LTL
X
| •   | p = “in | the | neXt |     | state, |     | p”  |     |     |
| --- | ------- | --- | ---- | --- | ------ | --- | --- | --- | --- |
p
F
| •   | p = “Finally |     | (sooner |     |     | or  | later) | p”  |     |
| --- | ------------ | --- | ------- | --- | --- | --- | ------ | --- | --- |
p
G
|     | = “Globally |     |     | (always) |     |     | p”  |     |     |
| --- | ----------- | --- | --- | -------- | --- | --- | --- | --- | --- |
| •   | p           |     |     |          |     |     |     |     |     |
|     | p           |     | p   |          | p   |     | p   |     |     |
U
| • (p | q) = | “p  | Until |     | q (and |     | sooner | or later | q)” |
| ---- | ---- | --- | ----- | --- | ------ | --- | ------ | -------- | --- |
W
| (p  | q)  | = “p | unless |     | q   | (or | always | p)” |     |
| --- | --- | ---- | ------ | --- | --- | --- | ------ | --- | --- |
|     | p   |      | p      |     | p   |     | q      |     |     |
24
compiledApril19,2012—⃝c
CharlesPecheur2005–p.20/33

The state explosion problem
The Dining Philosophers
Example: dining philosophers 3 2
2
3 1
4
1
Looking for deadlock with SPIN 4 0
! A classic!
! Dijkstra 1968 0
max depth 9,999 ! For any N philosophers
! Here N = 5
Sep 2007 © Charles Pecheur, Université catholique de Louvain 5
5 phils+forks 145 states, deadlock found
10 phils+forks 18,313 states, error trace too long
15 phils+forks 148,897 states, error trace too long
K processes with N states each = NK global states
25

The model correspondence problem
Consistency between model and program?
• Model extracted from the program
⇒
verify the extraction procedures (once for all)
Challenge: right level of detail
all details Þ state space explosion
missing details Þ “false alarm” reports
• Program generated from the model
⇒
verify the generation procedures (once for all)
Most applicable within well-­‐understood domains
• Model written (partially or entirely) by hand
⇒
check conformance by (model-­‐based) testing
26

Granularity	  of	  modeling
Granularity of modeling Analysis of different models
| Coarse | grain	  (Java) |     | Fine	  grain	  (bytecode) |     |     |        |        |
| ------ | --------------- | --- | --------------------------- | --- | --- | ------ | ------ |
|        |                 |     |                             |     |     | RacerP | RacerQ |
we can find the
(a)
t = i;
race only with
|     | (a) | (w) |     | (a) | (w) |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
fine-grain models
(b)
|     |     |     |     | t=i; | u=i; | t = t+1; |     |
| --- | --- | --- | --- | ---- | ---- | -------- | --- |
|     |     |     |     | (b)  | (x)  |          | (w) |
u = i;
|     | i = i+1 | i = i+1 |     | t=t+1; | u=u+1; |     |     |
| --- | ------- | ------- | --- | ------ | ------ | --- | --- |
(x)
u = u+1;
|     |     |     |     | (c) | (y) |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
(y)
i = u;
|     |     |     |     | i=t; | i=u; |     |     |
| --- | --- | --- | --- | ---- | ---- | --- | --- |
(c)
|     | (d) | (z) |     | (d) | (z) | i = t; |     |
| --- | --- | --- | --- | --- | --- | ------ | --- |
(z)
(d)
|     |     |     |     | E   | E   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     | E   | E   |     |     |     |     |     |
27
(c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 21 (c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 22
Looking for the appropriate granularity Example
• Compilers may rearrange the order of instruction • Suppose we use the double-check idiom only
– a simple store of a value into a memory cell may be compiled for lazy initialization
into a store into a local register, with the actual store to
• It would still be wrong, but…
memory appearing later (or not at all)
– Two loads or stores to different memory locations may be
• it is unlikely we would discover the flaw
reordered for reasons of efficiency
through finite state verification:
– Parallel computers may place values initially in the cache
memory of a local processor, and only later write into a – Spin assumes that memory accesses occur in the
memory area
order given in the Promela program, and ...
• Even representing each memory access as an individual
– we code them in the same order as the Java
action is not always sufficient!
program, but …
– Java does not guarantee that they will be executed
in that order
(c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 23 (c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 24

Granularity:	  data	  race
We can find the race only with fine-grain models
Granularity of modeling Analysis of different models
RacerP
|     |     |     |     |     | RacerQ | i   | RacerP.t | RacerQ.t |
| --- | --- | --- | --- | --- | ------ | --- | -------- | -------- |
we can find the
|     |     |     |     | (a) |     | 10  | –   | –   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
t = i;
race only with
| (a) | (w) | (a) | (w) |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | 10  | 10  | –   |
fine-grain models
(b)
t = t+1;
|     |     | t=i; | u=i; |     |     | 10  | 11  | –   |
| --- | --- | ---- | ---- | --- | --- | --- | --- | --- |
|     |     | (b)  | (x)  |     | (w) |     |     |     |
u = i;
|         |         |        |        |     |     | 10  | 11  | 10  |
| ------- | ------- | ------ | ------ | --- | --- | --- | --- | --- |
| i = i+1 | i = i+1 |        |        |     |     |     |     |     |
|         |         | t=t+1; | u=u+1; |     |     |     |     |     |
(x)
u = u+1;
|     |     |     |     |     |     | 10  | 11  | 11  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | (c) | (y) |     |     |     |     |     |
|     |     |     |     |     | (y) | 11  | 11  | 11  |
i = u;
|     |     | i=t; | i=u; |     |     |     |     |     |
| --- | --- | ---- | ---- | --- | --- | --- | --- | --- |
(c)
| (d) | (z) | (d) | (z) | i = t; |     |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- |
|     |     |     |     |        |     | 11  | 11  | 11  |
(z)
(d)
| E   | E   | E   | E   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
(c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 21 (c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 22
28
Looking for the appropriate granularity Example
• Compilers may rearrange the order of instruction • Suppose we use the double-check idiom only
– a simple store of a value into a memory cell may be compiled for lazy initialization
into a store into a local register, with the actual store to
• It would still be wrong, but…
memory appearing later (or not at all)
– Two loads or stores to different memory locations may be
• it is unlikely we would discover the flaw
reordered for reasons of efficiency
through finite state verification:
– Parallel computers may place values initially in the cache
memory of a local processor, and only later write into a – Spin assumes that memory accesses occur in the
memory area
order given in the Promela program, and ...
• Even representing each memory access as an individual
– we code them in the same order as the Java
action is not always sufficient!
program, but …
– Java does not guarantee that they will be executed
in that order
(c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 23 (c) 2007 Mauro Pezzè & Michal Young  Ch 8, slide 24

Granularity trade-­‐offs
Granularity = what operations are considered atomic
⇒
Finer granularity (memory access)
more precise (more behaviours), more costly (more states)
⇒
Coarser granularity (memory access)
less precise (less behaviours), less costly (less states)
Even representing each memory access is not always sufficient!
Compilers may rearrange the order of instructions
29

INTENSIONAL MODELS
30

Intensional models
Enumerating (and storing) all reachable states:
costly, limiting factor of finite state verification
Alternative: intensional (symbolic)
representations
describe sets of reachable states without
enumerating each one individually
Example (set of Integers)
Explicit: {2, 4, 6, 8, 10, 12, 14, 16, 18}
Intensional: {xÎN | x mod 2 = 0 and 0 < x < 20}
31

Intensional representations: size
Intensional representations may be more compact than the
set they represent
{xÎN | x mod 2 = 0 and 0 < x < 20} (10 elem)
{xÎN | x mod 2 = 0 and 0 < x < 1000} (500 elem)
Only because of structure or regularity in the set that is
captured by the representation!
Unstructured, irregular sets will necessarily have a larger
intensional representation
Information theory: representing subsets of N elements (2N
possibilities) requires O(N) bits in average
Enumeration is optimal in average!
32

A useful intensional model: BDD
(Reduced Ordered) Binary Decision Diagrams
A compact representation of Boolean functions
A BDD = a binary decision tree
a
with a fixed order on the variables
with merged identical subtrees
b
= a DAG
c
Canonical form:
the BDD for a function is unique
1 0
=> decide f º g in constant time
(using hash table)
∨ ⇒
(a b) c
33

Symbolic	  model	  with	  BDDs
A	  state =	  values of	  Boolean	  variables	  x …	  x
|     | 1   | n   |     |     |
| --- | --- | --- | --- | --- |
A	  set	  of	  states	  =	  a	  Boolean	  function f(x …	  x )
|     | 1   | n   |     |     |
| --- | --- | --- | --- | --- |
true	  if	  x …	  x is	  in	  the	  set
1 n
A	  transition =	  a	  pair	  of	  states	  x …	  x , x' …	  x'
| 1   | n 1 |     | n   |     |
| --- | --- | --- | --- | --- |
A	  transition	  relation	  =	  a	  function T(x …	  x , x' …	  x' )
|     | 1   | n   | 1   | n   |
| --- | --- | --- | --- | --- |
true	  if	  there	  is	  a	  transition	  between	  x …	  x and	   x' …	  x'
|     | 1 n |     | 1   | n   |
| --- | --- | --- | --- | --- |
34

| Symbolic | model	  checking |     |     | with | BDDs |
| -------- | ----------------- | --- | --- | ---- | ---- |
Operations	  can	  be	  efficiently	  computed	  on	  BDDs
| ∧ ∨               | ∃      | ∀       |     |     |     |
| ----------------- | ------ | ------- | --- | --- | --- |
| ,	   ,	  ¬,	   | x,	   | x,	  … |     |     |     |
Compute	  the	  BDD	  of	  the	  reachable	  state	  space
iteratively,	  breadth-­‐first:
the	  BDD	  of	  states	  reachable	  in	  k+1	  steps
from	  the	  BDD	  of	  states	  reachable	  in	  k steps
stabilizes	  when	  all	  states	  in	  the	  next	  step
are	  already	  in	  the	  current	  step
|                 |         | ∨∃  | ∧                          |        |     |
| --------------- | ------- | --- | -------------------------- | ------ | --- |
| S (x)	  =	  S | (x)	   |     | x'	  .	  T(x',	  x)	   | S (x') |     |
| k+1             | k       |     |                            | k      |     |
35

Symbolic model checking: properties
A temporal logic property can also be transformed into Boolean
variables and transitions, represented as BDDs
Combine BDD representations of model and property
to produce a representation of just the set of transitions leading
to a violation of the property
If the set is empty, the property has been verified
36

MODEL REFINEMENT
37

Model refinement
Construction of finite state models
balancing precision and efficiency
Often the first model is unsatisfactory
report unfeasible failures
exhaust resources before producing any result
Idea: improve the model and restart
Finite state verification as iterative process
38

Iterative process
construct an
initial model
attempt verification
exhausts
spurious
computational
valid
results
resources
results
abstract the model make the model
further more precise
report
results
39

M1
M2
Mk
Model refinement
S
⊨
S P ? real program S, property P
⊨
M P ? initial (coarse grain) model M
1 1
⇒
spurious counter example, in M but not in S
1
⊨
M P ? refined (more detailed) model M
2 2
⇒
spurious counter example, in M but not in S
2
....
⊨
M P ? last refined model M
k k
⇒
valid counter example, in M and in S
k
40

Another	  refinement	  approach:
add	  premises	  to	  the	  property
⊨
| S	   P       | ?                                     | real	  program |     |
| ------------- | ------------------------------------- | --------------- | --- |
| M	   ⊨ P	   | initial	  (coarse	  grain)	  model |                 |     |
⇒
spurious	  counter	  example,	  in	  M	  but	  not	  in	  S
⇒
add	  a	  constraint	  C that	  eliminates	  the	  bogus
1
behavior
| M	   ⊨ C | ⇒   | P   | refined	  (more	  detailed)	  model |
| --------- | --- | --- | -------------------------------------- |
1
⇒
spurious	  counter	  example,	  in	  M but	  not	  in	  M
1
⇒
add	  a	  constraint	  C that	  eliminates	  the	  bogus
2
behavior
| ⊨        | ∧   | ⇒       |     |
| -------- | --- | ------- | --- |
| M	   (C |     | C )	   | P   |
|          | 1   | 2       |     |
......	  until	  the	  verification	  succeeds	  or	  produces	  a	  valid	  counter
example
42

DATA MODEL VERIFICATION
43

Data model verification
Many information systems are characterized by
simple program logic and algorithms
complex data structures
A key element is the data model
(class and object diagrams + OCL assertions)
= sets of data and relations among them
Challenge: prove that
individual constraints are consistent
together they ensure the desired properties of the system as
a whole
44

Data Model Verification
Complex data models
Same general verification principles
systematic analysis of models
thorough testing is impractical
Difficulty: consider all the possible combinations
of choices in a complex data model
45

Example:	  a	  simple	  web	  site
Signature	  =	  Sets	  +	  Relations
A	  set of	  pages	  divided	  among	  restricted,	  unrestricted,	  maintenance pages
unrestricted	  pages:	  freely	  accessible
restricted	  pages:	  accessible	  only	  to	  registered	  users
maintenance	  pages:	  inaccessible	  to	  both	  sets	  of	  users
A	  set of	  users:	  	  administrator,	  registered,	  and	  unregistered
| A	  set	  of	  links | relations                           | among	  pages |       |
| ----------------------- | ----------------------------------- | -------------- | ----- |
| private                 | links	  lead	  to	  restricted   |                | pages |
| public                  | links	  lead	  to	  unrestricted |                | pages |
Maintenance	  links	  lead	  to	  maintenance pages
A	  set	  of	  access	  rights relations between	  users	  and	  pages
| unregistered	  users |     | can	  access	  only	  unrestricted	  pages |     |
| --------------------- | --- | ---------------------------------------------- | --- |
registered users	  can	  access	  both	  restricted	  and	  unrestricted	  pages
administrator can	  access	  all	  pages	  including	  maintenance	  pages
46

Web site: constraints
Example constraints for the web site:
No self loops from links relations
At most one type of link between two pages
NOTE: relations need not be symmetric:
<A, B> ¹ <B, A>
Web site must be connected
...
47

Data model verification and relational algebra Example: a simple web site
Signature = Sets + Relations
• Many information systems are characterized by
• A set of pages divided among restricted, unrestricted, maintenance
pages
– simple logic and algorithms
– unrestricted pages: freely accessible
– complex data structures
– restricted pages: accessible only to registered users
– maintenance pages: inaccessible to both sets of users
• Key element of these systems is the data model
• A set of users: administrator, registered, and unregistered
(UML class and object diagrams + OCL assertions)
• A set of links relations among pages
sets of data and relations among them
=
– private links lead to restricted pages
– public links lead to unrestricted pages
• The challenge is to prove that
– Maintenance links lead to maintenance pages
– individual constraint are consistent and
• A set of access rights relations between users and pages
– unregistered users can access only unrestricted pages
– together they ensure the desired properties of the
– registered users can access both restricted and unrestricted pages
system as a whole
– administrator can access all pages including maintenance pages
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 37 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 38
Web site: data model
Complete a specification with constraints
The data model for the simple web site
users page
Example constraints for the web site:
• Exclude self loops from links relations
• Allow at most one type of link between two
unregistered unrestricted
maintenance
public
pages
private
– NOTE: relations need not be symmetric: registered public restricted
administrator maintenance
private
<A, B> # <B, A> maintenance
• Web site must be connected
LEGEND
• ...
A A B
Set B
r
specializes
set A
B There is a relation r
between sets A and B
48
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 39 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 40

| Alloy:	  a	  relational  |     |     | modelling     |     | language |
| -------------------------- | --- | --- | ------------- | --- | -------- |
| In	  Alloy,	  everything |     | is  | a	  relation |     |          |
scalars,	  functions,	  tuples,	  sets,	  .	  .	  .
| A	  relation	  is      | a	  table                    |     |                                  |     |     |
| ------------------------ | ----------------------------- | --- | -------------------------------- | --- | --- |
| a	  set	  of	  tuples | of	  atoms                   |     |                                  |     |     |
| Relational               | operations                    |     | (union,	  inter,	  join,	  …) |     |     |
| Quantifiers              | (all,	  some,	  none,	  …) |     |                                  |     |     |
Object-­‐orientation	  (encapsulation,	  inheritance)
| The	  Alloy | Verifier | can | verify | properties | on	  Alloy |
| ------------ | -------- | --- | ------ | ---------- | ----------- |
specifications
49

Web site in Alloy: Page
module WebSite
signature:
Set Page
// Pages include three disjoint sets of links
sig Page {disj linksPriv, linksPub, linksMain: set Page }
constraints
// Each type of link points to a particular class of page Introduce
fact connPub {all p:Page, s: Site | p.linksPub in s.unres } relations
fact connPriv {all p:Page, s: Site | p.linksPriv in s.res }
fact connMain {all p:Page, s: Site | p.linksMain in s.main }
// Self loops are not allowed
fact noSelfLoop {no p:Page| p in p.linksPriv+p.linksPub+p.linksMain }
50

Web site in Alloy: User
// Users are characterized by the set of pages that they can access
sig User {pages: set Page }
// Users are partitioned into three sets
part sig Administrator, Registered, Unregistered extends User {}
// Unregistered users can access only the home page, and unrestricted pages
fact accUnregistered {
all u: Unregistered, s: Site|u.pages = (s.home+s.unres)
}
// Registered users can access the home page,restricted and unrestricted pages
fact accRegistered {
all u: Registered, s: Site|u.pages = (s.home+s.res+s.unres)
}
// Administrators can access all pages
fact accAdministrator {
all u: Administrator, s: Site|
u.pages = (s.home+s.res+s.unres+s.main)
}
Constraints map
users to pages
51

Analyzing relational algebra
specifications
In general, specifications have an infinite set of models
First-­‐order logic, undecidable
⇒
Overconstrained no model
⇒
Underconstrained undesired models
Check properties over a finite set of small models
by limiting the cardinality of the sets
e.g. 5 pages, 3 users, 10 links
Small scope hypothesis: a (counter) example that
invalidates a property can usually be found within a small
model
52

Checking	  a	  finite	  set	  of	  models
1.	  Check	  existence	  of	  models	  (command	  run)
⊨
| Find	  M	  such	  that	  M	   | Program |     |
| ---------------------------------- | ------- | --- |
If	  not	  found:	  there	  are	  logical	  contradictions	  in	  the
specification,	  it	  is	  overconstrained
2.	  Check	  properties (command	  check)
|                                    | ⊨ ∧         |           |
| ---------------------------------- | ----------- | --------- |
| Find	  M	  such	  that	  M	   | Program	   | ¬Property |
If	  no	  counterexample	  found:	  no	  violation	  exist	  within
the	  small	  models
BUT	  NOT	  that	  NO	  violation	  exists	  at	  all!
53

Web site in Alloy: analysis
run init for 5 Cardinality limit:
Consider up to
5 objects of each type
// can unregistered users
// visit all unrestricted pages?
assert browsePub { Any unrestricted page of a site is connected
to the home page through a path of public links
all p: Page, s: Site|
p in s.unres implies s.home in p.* linksPub
}
check browsePub for 3
*
Transitive closure
(including home)
54

Checking a finite set of solutions Analysis of the web site specification
• If an example is found:
run init for 5 Cardinality limit:
– There are no logical contradictions in the model Consider up to
5 objects of each type
// can unregistered users
– The solution is not overconstrained
// visit all unrestricted pages?
• If no counterexample of a property is found:
assert browsePub { Property to be
checked
all p: Page, s: Site|
– no reasonably small solution (property violation)
p in s.unres implies s.home in p.* linksPub
exists
}
– BUT NOT that NO solution exists check browsePub for 3
• We depend on a “small scope hypothesis”: Most bugs that
can cause failure with large collections of objects can also
*
cause failure with very small collections (so it’s worth Transitive closure
(including home)
looking for bugs in small collections even if we can’t afford
to look in big ones)
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 45 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 46
Analysis result
Analysis result Correcting the specification
CoCuonutnetreerxeaxmamplpel:e: • We can eliminate the problem by eliminating public
• UUnrnergeigsitsetreerde dU sUesre_r2_ 2cannot links from maintenance or reserved pages:
vicsaitn tnhoet uvnisriets tthriected page
unrestricted page page_2
page_2
fact descendant {
• The only path from the
The only path from the home
all p:Pages, s:Site|p in s.main+s.res
home page to page_2
page to page_2 goes through
implies no p. links.linkPub
goes through the
the restricted page page_0
restricted page page_0 }
The property is violated
• The property is violated • Analysis would find no counterexample of cardinality 3
because unrestricted browsing
because unrestricted
• We cannot conclude that no larger counter-example
paths can be interrupted by
browsing paths can be
restricted pages or pages exists, but we may be satisfied that there is no reason
interrupted by restricted
unpdaeger sm oari nptaegneasn ucneder to expect this property to be violated only in larger
maintenance models
(c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 47 (c) 2007 Mauro Pezzè & Michal Young Ch 8, slide 48
Ch 8, slide 55

Summary
Finite	  state	  verification is complementary to	  testing
Can	  find bugs that are	  extremely hard	  to	  test	  for	  (concurrency,	  race
conditions)
|          | But       | is limited |      | in	  scope	  (not                   |     | all kinds      | of	  errors) |     |
| -------- | --------- | ---------- | ---- | ------------------------------------- | --- | -------------- | ------------- | --- |
| Checking |           | models     |      | can	  be	  (and	  is)	  automated |     |                |               |     |
| But      | designing |            | good | models                                |     | is challenging |               |     |
consider abstraction,	  granularity,	  properties to	  be	  checked
Iterative	  refinement
|             | model,	  check,	  refine |     |                     |     | until  | a	  useful | result | is obtained |
| ----------- | -------------------------- | --- | ------------------- | --- | ------ | ----------- | ------ | ----------- |
| Intensional |                            |     | models              |     |        |             |        |             |
|             | represent                  |     | set	  of	  states |     | (BDDs) |             |        |             |
Data	  model	  verification
|     | finite	  state	  applied |     |     |     | to	  data	  models |     |     |     |
| --- | -------------------------- | --- | --- | --- | -------------------- | --- | --- | --- |
relational specifications,	  verification in	  small	  model	  scope
57

References
[PY] M. Pezzè and Michal Young, Software
Testing and Analysis: Process, Principles, and
Techniques, Wiley, 2008.
Ch. 8
58

Software Quality Assurance
8 – Software Measurement
Charles Pecheur
Apr 2018
1

|                    | Why | software measurement |         |                     |              |     |             |
| ------------------ | --- | -------------------- | ------- | ------------------- | ------------ | --- | ----------- |
| Software quality   |     |                      |         | assurance =         |              |     |             |
| assess             |     | and improve          |         |                     | the quality  |     | of software |
| The first step     |     |                      | towards |                     | quality      | is  |             |
| to understand      |     |                      | what    |                     | it is        |     |             |
| and how to measure |     |                      |         |                     | it           |     |             |
| You cannot         |     | predict              |         |                     | nor control  |     |             |
| what               | you | cannot               |         | measure. (DeMarco)  |              |     |             |
2

Software measurement
| Software measurement |                 | =                      |     |       |
| -------------------- | --------------- | ---------------------- | --- | ----- |
| deriving             | a numeric       | value for an attribute |     | of a  |
| software product     |                 | or process.            |     |       |
| Allows               | for comparisons |                        |     |       |
A fundamental part of Software Engineering
| Metric           | =              |             |               |       |
| ---------------- | -------------- | ----------- | ------------- | ----- |
| a means          | of measurement |             | of a property | of a  |
| software product |                | or process. |               |       |
3

Objectives of software measurement
| Understand, Control, Improve |                              |          | the quality    | of           |
| ---------------------------- | ---------------------------- | -------- | -------------- | ------------ |
| software Products            | and Processes                |          |                |              |
|                              |                              | Control  | Improve        |              |
|                              | Product                      | ISO 9126 | best practices |              |
|                              | Process                      | ISO 9001 | CMM            |              |
| • Internal                   | attributes: size, complexity |          |                | (structural) |
•
| External | attributes: quality, reliability |     |     | (functional) |
| -------- | -------------------------------- | --- | --- | ------------ |
4

Goal-Question-Metric
Every measurement responds to a goal or a need
1. Goals of the project
2. Questions to be answered to assess whether the goals are
being met
A Goal-Based Framework for Software Measurement ◾ 101
3. Metrics to be measured to answer the questions
Goal: Evaluate the effectiveness of an organization’s coding standard.
Questions: Who is using the What is the productivity What is the quality
standard? of the coders? of the code?
…
Effort Errors
Proportion of coders Experience of coders Code size
Metrics: — Using the standard, — With the standard, — Lines of code,
— Using the language. — With the language, — Number of classes,
— With the environment, — Number of methods,
etc. — Function points,
etc.
5
FIGURE 3.2 Example of deriving metrics from goals and questions.
code produced by following the standard is superior in some way to code
produced without it. To decide whether the standard is effective, you must
ask several key questions. First, it is important to know who is using the
standard, so that you can compare the productivity of the coders who use
the standard with the productivity of those who do not. Likewise, you
probably want to compare the quality of the code produced with the stan-
dard with the quality of non-standard code.
Once these questions are identified, you must analyze each question
to determine what must be measured in order to answer the question.
For example, to understand who is using the standard, it is necessary to
know what proportion of coders is using the standard. However, it is also
important to have an experience profile of the coders, explaining how long
they have worked with the standard, the environment, the language, and
other factors that will help to evaluate the effectiveness of the standard.
The productivity question requires a definition of productivity, which is
usually some measure of effort divided by some measure of product size.
As shown in Figure 3.2, the metric can be in terms of LOCs, function
points, or any other metric that will be useful to you. Similarly, quality
may be measured in terms of the number of errors found in the code, plus
any other quality measures that you would like to use.
In this way, you generate only those measures that are related to the
goal. Notice that, in many cases, several measurements may be needed
to answer a single question. Likewise, a single measurement may apply
to more than one question. The goal provides the purpose for collect-
ing the data, and the questions tell you and your project how to use the
data.

|                   | Measurement |      |             | objectives             |       |          |     |
| ----------------- | ----------- | ---- | ----------- | ---------------------- | ----- | -------- | --- |
| Managers          |             |      |             | Engineers              |       |          |     |
| • What            | does        | each | process     | • Are the requirements |       |          |     |
| cost?             |             |      |             | testable?              |       |          |     |
| •                 |             |      |             | •                      |       |          |     |
| How productive is |             |      | the staff?  | Have we                | found | all the  |     |
faults?
| • How good is      |               | the code being |           |           |             |         |     |
| ------------------ | ------------- | -------------- | --------- | --------- | ----------- | ------- | --- |
| developed?         |               |                |           | • Have we | met our     | product | or  |
|                    |               |                |           | process   | goals?      |         |     |
| • Will the user be |               |                | satisfied |           |             |         |     |
| with               | the product?  |                |           | • What    | will happen | in the  |     |
future?
| • How can | we  | improve?  |     |     |     |     |     |
| --------- | --- | --------- | --- | --- | --- | --- | --- |
6

What is a measurement?
size: 30x30x50 cm
volume: 45 l
weight: 3.42 kg
size: ?
?
cost: ?
reliability: ?
8

Measurement
| Measurement   |     | = mapping     |        |             |      |
| ------------- | --- | ------------- | ------ | ----------- | ---- |
| from          |     | the empirical | world  |             |      |
| to the formal |     |               | world  |             |      |
| objects       |     | A             |        | to  numbers | M(A) |
| domain        |     |               |        | to range    |      |
relations A bigger than B to relations The Basics of Measurement  M(A) > M(B)   ◾    35
| Measure |     | = number   | associated | to an entity |               |
| ------- | --- | ---------- | ---------- | ------------ | ------------- |
|         |     | Real world |            |              | Number system |
M
Joe
Fred
63 72
|     | Joe taller than Fred |     |                      |     | M(Joe) > M(Fred)   |
| --- | -------------------- | --- | -------------------- | --- | ------------------ |
|     | Empirical relation   |     | Preserved under M as |     | Numerical relation |
9
FIGURE 2.4  Representation condition.
This statement means that:
•  Whenever Joe is taller than Fred, then M(Joe) must be a bigger num-
ber than M(Fred).
•  We can map Jill to a higher number than Jack only if Jill is taller than
Jack.
EXAMPLE 2.5
In  Section  2.1.1,  we  noted  that  there  can  be  many  relations  on  a  given
set,  and  we  mentioned  several  for  the  attribute  height.  The  representa-
tion condition has implications for each of these relations. Consider these
examples:
For the (binary) empirical relation taller than, we can have the numerical
relation
  x > y
Then, the representation condition requires that for any measure M,
  A taller than B if and only if M(A) > M(B)

For  the  (unary)  empirical  relation  is-tall,  we  might  have  the  numerical
relation
  x > 70
The representation condition requires that for any measure M,
  A is-tall if and only if M(A) > 70

The Basics of Measurement   ◾   31
Likert Scale
Give the respondent a statement with which to agree or disagree. Example:
This software program is reliable.
|     |     |     |     |     |     |     |     | Strongly  |     |     |     | Neither agree  |     |     |     |     |     | Strongly  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --------- | --- |
The Basics of Measurement   ◾   31
|     |     |     |     |     |     |     |     | Agree |     | Agree |     | nor disagree |     |     |     | Disagree |     | Disagree |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ----- | --- | ------------ | --- | --- | --- | -------- | --- | -------- | --- |
Forced Ranking
Likert Scale Give n alternatives, ordered from 1 (best) to n (worst). Example:
Give the respondent a statement with which to agree or disagree. Example: Rank the following five software modules in order of maintenance diffi-
This software program is reliable. culty, with 1 = least complex, 5 = most complex:
|     |                |     |       |     |                |     |     |          |     |           |     | —   |     | Module A |     |     |     |     |     |
| --- | -------------- | --- | ----- | --- | -------------- | --- | --- | -------- | --- | --------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
|     | Strongly       |     |       |     | Neither agree  |     |     |          |     | Strongly  |     |     |     |          |     |     |     |     |     |
|     |                |     |       |     |                |     |     |          |     |           |     | —   |     | Module B |     |     |     |     |     |
|     | Agree          |     | Agree |     | nor disagree   |     |     | Disagree |     | Disagree  |     |     |     |          |     |     |     |     |     |
|     |                |     |       |     |                |     |     |          |     |           |     | —   |     | Module C |     |     |     |     |     |
|     | Forced Ranking |     |       |     |                |     |     |          |     |           |     | —   |     | Module D |     |     |     |     |     |
Measurement: range
Give n alternatives, ordered from 1 (best) to n (worst). Example: — Module E
Rank the following five software modules in order of maintenance diffi-
Verbal Frequency Scale
culty, with 1 = least complex, 5 = most complex: The Basics of Measurement   ◾   31
|     |     |     |     |     |     |          |     | Example: How often does this program fail? |     |     |       |     |           |     | The Basics of Measurement   ◾   31   |        |     |     |       |
| --- | --- | --- | --- | --- | --- | -------- | --- | ------------------------------------------ | --- | --- | ----- | --- | --------- | --- | ------------------------------------ | ------ | --- | --- | ----- |
|     |     |     |     |     | —   | Module A |     |                                            |     |     |       |     |           |     |                                      |        |     |     |       |
|     |     |     |     |     |     |          |     | Always                                     |     |     | Often |     | Sometimes |     |                                      | Seldom |     |     | Never |
• Real numbers
|     |     |     |     |     | —   | Module B |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Likert Scale
Likert Scale Ordinal Scale
— Module C Give the respondent a statement with which to agree or disagree. Example:
Give the respondent a statement with which to agree or disagree. Example: List several ordered alternatives and have respondents select one. For example:
• Integer numbers — Module D This software program is reliable.
This software program is reliable. How often does the software fail?
|     |     |     |     |     | —   | Module E |           |                       |     |     |     |                |     |     |     |     |     |           |     |
| --- | --- | --- | --- | --- | --- | -------- | --------- | --------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --------- | --- |
|     |     |     |     |     |     |          | Strongly  |                       |     |     |     | Neither agree  |     |     |     |     |     | Strongly  |     |
|     |     |     |     |     |     |          |           |   Strongly  1. Hourly |     |     |     | Neither agree  |     |     |     |     |     | Strongly  |     |
•
|     | Symbols |     |     |     |     |     | Agree |     |     | Agree |     | nor disagree |     |     | Disagree |     |     | Disagree |     |
| --- | ------- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- | --- | ------------ | --- | --- | -------- | --- | --- | -------- | --- |
Verbal Frequency Scale Agree Agree nor disagree Disagree Disagree
  2. Daily
Example: How often does this program fail?
Forced Ranking   3. Weekly
Forced Ranking
Examples:
|     | Always |     | Often |     |     | Sometimes | Give n alternatives, ordered from 1 (best) to n (worst). Example: | Seldom |     |     | Never |     |     |     |     |     |     |     |     |
| --- | ------ | --- | ----- | --- | --- | --------- | ----------------------------------------------------------------- | ------ | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Give n alternatives, ordered from 1 (best) to n (worst). Example:   4. Monthly
Rank the following five software modules in order of maintenance diffi-
Rank the following five software modules in order of maintenance diffi-
Ordinal Scale
culty, with 1 = least complex, 5 = most complex:   5. Several times a year
culty, with 1 = least complex, 5 = most complex:
List several ordered alternatives and have respondents select one. For example:
  6. Once or twice a year
|     | How often does the software fail? |     |     |     |     |     |     |     |     |     |     | —   |     | Module A |     |     |     |     |     |
| --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
|     |                                   |     |     |     |     |     |     |     |     |     |     | —   |     | Module A |     |     |     |     |     |
  7. Never
|     |     |     |     |     |     |     |     |     |     |     |     | —   |     | Module B |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |     |     |     | —   |     | Module B |     |     |     |     |     |
  1. Hourly
|     |            |     |     |     |     |     |     | Comparative Scale |     |     |     | —               |     | Module C |     |     |               |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --------------- | --- | -------- | --- | --- | ------------- | --- | --- |
|     |            |     |     |     |     |     |     |                   |     |     |     | —               |     | Module C |     |     |               |     |     |
|     |   2. Daily |     |     |     |     |     |     |                   |     |     |     |                 |     |          |     |     |               |     |     |
|     |            |     |     |     |     |     |     |                   |     |     |     | —               |     | Module D |     |     |               |     |     |
|     |            |     |     |     |     |     |     |                   |     |     |     | —               |     | Module D |     |     |               |     |     |
|     |            |     |     |     |     |     |     | Very superior     |     |     |     | About the same  |     |          |     |     | Very inferior |     |     |
|     |            |     |     |     |     |     |     |                   |     |     |     | —               |     | Module E |     |     |               |     |     |
  3. Weekly
|     |              |     |     |     |     |     |                        | 1   | 2   |     | 3   | 4  — | 5   | Module E | 6   | 7   |     | 8   |     |
| --- | ------------ | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | ---- | --- | -------- | --- | --- | --- | --- | --- |
|     |   4. Monthly |     |     |     |     |     | Verbal Frequency Scale |     |     |     |     |      |     |          |     |     |     |     |     |
Verbal Frequency Scale
Numerical Scale
Example: How often does this program fail?
  5. Several times a year Example: How often does this program fail?
|     |     |     |     |     |     |     |     | Unimportant  |     |     |       |     |           |     |     |        | Important |       |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | ----- | --- | --------- | --- | --- | ------ | --------- | ----- | --- |
|     |     |     |     |     |     |     |     | Always       |     |     | Often |     | Sometimes |     |     | Seldom |           | Never |     |
  6. Once or twice a year Always Often Sometimes Seldom Never
|     |            |     |     |     |     |     |               | 1   | 2   |     | 3   | 4   | 5   |     | 6   | 7   |     | 8   |     |
| --- | ---------- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |   7. Never |     |     |     |     |     | Ordinal Scale |     |     |     |     |     |     |     |     |     |     |     |     |
Ordinal Scale
List several ordered alternatives and have respondents select one. For example:
|     |                   |     |     |     |     |     | FIGURE 2.2  | List several ordered alternatives and have respondents select one. For example: |     | Subjective rating schemes. |     |     |     |     |     |     |     |     |     |
| --- | ----------------- | --- | --- | --- | --- | --- | ----------- | ------------------------------------------------------------------------------- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | Comparative Scale |     |     |     |     |     |             | How often does the software fail?                                               |     |                            |     |     |     |     |     |     |     |     |     |

How often does the software fail?
|     | Very superior  |     |     | About the same  |     |     |     |     | Very inferior |     |     |     |     |     |     |     |     |     |     |
| --- | -------------- | --- | --- | --------------- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  1. Hourly
  1. Hourly
|     | 1   | 2   | 3   |     | 4   | 5   | 6   | 7   |     | 8   |     |     |     |     |     |     |     |     | 10  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  2. Daily
  2. Daily
  3. Weekly
Numerical Scale
  3. Weekly
  4. Monthly
|     | Unimportant  |     |     |     |     |     |      |   4. Monthly               | Important |     |     |     |     |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | ---- | -------------------------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1            | 2   | 3   |     | 4   | 5   | 6    | 5. Several times a year 7  |           | 8   |     |     |     |     |     |     |     |     |     |
  5. Several times a year
  6. Once or twice a year
  6. Once or twice a year
| FIGURE 2.2  |     | Subjective rating schemes. |     |     |     |     |     | 7. Never |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | --- | -------------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  7. Never
Comparative Scale
|     |     |     |     |     |     |     |     | Comparative Scale |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

|     |     |     |     |     |     |     |     | Very superior  |     |     | About the same  |                 |     |     |     |     | Very inferior |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --------------- | --------------- | --- | --- | --- | --- | ------------- | --- | --- |
|     |     |     |     |     |     |     |     | Very superior  |     |     |                 | About the same  |     |     |     |     | Very inferior |     |     |
|     |     |     |     |     |     |     |     | 1              | 2   | 3   |                 | 4               | 5   | 6   |     | 7   |               | 8   |     |
|     |     |     |     |     |     |     |     | 1              | 2   |     | 3               | 4               | 5   |     | 6   | 7   |               | 8   |     |
Numerical Scale
Numerical Scale
|     |     |     |     |     |     |     |             | Unimportant  |                            |                            |     |     |     |     |     |     | Important |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------------ | -------------------------- | -------------------------- | --- | --- | --- | --- | --- | --- | --------- | --- | --- |
|     |     |     |     |     |     |     |             | Unimportant  |                            |                            |     |     |     |     |     |     | Important |     |     |
|     |     |     |     |     |     |     |             | 1            | 2                          | 3                          |     | 4   | 5   | 6   |     | 7   |           | 8   |     |
|     |     |     |     |     |     |     |             | 1            | 2                          |                            | 3   | 4   | 5   |     | 6   | 7   |           | 8   |     |
|     |     |     |     |     |     |     | FIGURE 2.2  |              | Subjective rating schemes. |                            |     |     |     |     |     |     |           |     |     |
|     |     |     |     |     |     |     | FIGURE 2.2  |              |                            | Subjective rating schemes. |     |     |     |     |     |     |           |     |     |

Measurement: mapping
34 ◾ Software Metrics
Statement type
Must define precisely! Include Exclude
Executable
Nonexecutable
Example: LOC
Declarations
Compiler directives
Comments
On their own lines
On lines with source code
Can be direct or indirect
Banners and nonblank spacers
Blank (empty) comments
Ratios
Blank lines
How produced
density = mass / volume
Include Exclude
Programmed
Generated with source code generators
Converted with automatic translators
Copied or reused without change
Modified
Removed
11
Origin
Include Exclude
New work: no prior existence
Prior work: taken or adapted from
A previous version, build, or release
Commercial, off-the-shelf software, other than libraries
Government furnished software, other than reuse libraries
Another product
A vendor-supplied language support library (unmodified)
A vendor-supplied operating system or utility (unmodified)
A local or modified language support library or operating system
Other commercial library
A reuse library (software designed for reuse)
Other software component or library
FIGURE 2.3 Portion of US Software Engineering Institute checklist for lines-of-
code count.

PRODUCT METRICS: SIZE
12

Software size
| The main internal |     |     | attribute | for software: size |     |     |
| ----------------- | --- | --- | --------- | ------------------ | --- | --- |
Useful:
| 100,000 LOC harder to test, maintain |     |     |          |             | than | 1,000 LOC |
| ------------------------------------ | --- | --- | -------- | ----------- | ---- | --------- |
| 100,000 LOC likely                   |     |     | contains | more faults | than | 1,000 LOC |
Component to indirect attributes:
|     | productivity |         | = size / effort |              |     |     |
| --- | ------------ | ------- | --------------- | ------------ | --- | --- |
|     | defect       | density | = defect        | count / size |     |     |
How measured?
13

Size metrics
• Lines of code
•
Number of bytes
• Number of modules
• …
| Depends | on the question to be | answered |
| ------- | --------------------- | -------- |
complexity
| disk | footprint |     |
| ---- | --------- | --- |
…
| Should | be non-negative, zero | iff empty, additive |
| ------ | --------------------- | ------------------- |
14

Lines of code
Lines of code (LOCs)
| How are they |     | counted? |     |     |     |
| ------------ | --- | -------- | --- | --- | --- |
•
|     | Blank             | lines                  |     |     |     |
| --- | ----------------- | ---------------------- | --- | --- | --- |
| •   | Comments          |                        |     |     |     |
| •   | Data declarations |                        |     |     |     |
| •   | Several           | instructions on a line |     |     |     |
Consensus:
| NCLOC         | = no comments |             | nor           | blank lines,  |     |
| ------------- | ------------- | ----------- | ------------- | ------------- | --- |
| everything    |               | else counts | as 1 per line |               |     |
| Comment lines |               | can be      | useful        | to measure    | too |
| CLOC          | = lines       | of comments |               |               |     |
LOC = NCLOC + CLOC
| comment density |     | = CLOC / LOC |     |     |     |
| --------------- | --- | ------------ | --- | --- | --- |
15

Lines of code: what counts?
| What | files?               |     |     |                  |     |
| ---- | -------------------- | --- | --- | ---------------- | --- |
| •    | Program code         |     |     |                  |     |
| •    | Test drivers, stubs  |     |     |                  |     |
| •    | Prototypes deleted   |     |     | in final product |     |
•
|                               | Automatically |                             | generated |         | code                     |
| ----------------------------- | ------------- | --------------------------- | --------- | ------- | ------------------------ |
| •                             | Imported      | code                        |           |         |                          |
| Delivered                     |               | code or developed           |           |         | code?                    |
| Executable                    |               | statements                  |           | (ES) =  |                          |
| no blanks, comments, data nor |               |                             |           |         | headers, 1 per statement |
| Delivered                     |               | source instructions (DSI) = |           |         |                          |
no blanks, comments, 1 per statement or data declaration
16

|                         | Halstead's |                     |        |     | "software science" |       |          |       |
| ----------------------- | ---------- | ------------------- | ------ | --- | ------------------ | ----- | -------- | ----- |
|                         |            |                     |        |     |                    | y :=  | 1 ;      |       |
| An early                | approach   |                     | (1977) |     |                    |       |          |       |
|                         |            |                     |        |     |                    | i :=  | n ;      |       |
| Program P as a sequence |            |                     |        |     | of tokens:         | while | i > 0    | {     |
| operators               |            | or operands         |        |     |                    |       | y := y   | × i ; |
|                         |            |                     |        |     |                    |       | i := i – | 1 ;   |
| µ                       | = number   | of unique operators |        |     |                    |       |          |       |
1
}
| µ   | = number | of unique operands |     |     |     |     |     |     |
| --- | -------- | ------------------ | --- | --- | --- | --- | --- | --- |
2
|     |                                  |     |     |     |     | return | y ; |     |
| --- | -------------------------------- | --- | --- | --- | --- | ------ | --- | --- |
| N   | = total occurrences of operators |     |     |     |     |        |     |     |
1
| N   | = total occurrences of operands |     |     |     |     |     |     |     |
| --- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- |
2
|            |       |       |       |     |     | N1 = 9 | μ1 = 6    |      |
| ---------- | ----- | ----- | ----- | --- | --- | ------ | --------- | ---- |
|            |       |       |       |     |     | N2 =   | 13 μ2 = 5 |      |
| Length     | of P: |       | N = N |     | + N |        |           |      |
|            |       |       |       |     | 1 2 |        |           |      |
| Vocabulary |       | of P: | µ = µ |     | + µ | N =    | 22 μ      | = 11 |
|            |       |       |       |     | 1 2 |        |           |      |
Volume of P: V = N × log µ (number of bits) V = 22 × 3.46 = 76.1
2
| … and others |     | (not valid |     | measures; not additive) |     |     |     |     |
| ------------ | --- | ---------- | --- | ----------------------- | --- | --- | --- | --- |
17

Alternative metrics
| • Number   | of (storage) bytes          |             |
| ---------- | --------------------------- | ----------- |
| easy       | to find                     | (file size) |
| • Number   | of (source code) characters |             |
| easy       | to find                     | (wc)        |
| • Weighted |                             | LOC         |
1 LOC of LISP = α LOC of C
| Non-text | code?                        |     |
| -------- | ---------------------------- | --- |
| visual   | programming, GUI builders, … |     |
18

Design size
Number of elements
Procedural languages:
•
procedures, functions
| • procedure     | parameters | (interface size) |     |
| --------------- | ---------- | ---------------- | --- |
| Object-oriented | languages  |                  |     |
•
packages, classes
• design pattern types, instances
• public methods, attributes
| • public method | parameters, overloaded |     | versions |
| --------------- | ---------------------- | --- | -------- |
Requirements, specifications
• statements, classes, clauses, …
| • diagram     | elements           |     |     |
| ------------- | ------------------ | --- | --- |
| • pages (both | text and graphics) |     |     |
19

Functional size
| Measure  | amount | of functionality: |     |     |
| -------- | ------ | ----------------- | --- | --- |
| function |        | points (FP)       |     |     |
Useful:
| •   | to estimate | development |     | effort and duration (mm/FP) |
| --- | ----------- | ----------- | --- | --------------------------- |
•
|              | to express defect   |          | density | (defects/FP) |
| ------------ | ------------------- | -------- | ------- | ------------ |
| •            | to bill development |          | ($/FP)  |              |
| • Albrecht's |                     | Function | points  |              |
•
COCOMO II
20

|     | Function |     | points: example |     |     |     |     |
| --- | -------- | --- | --------------- | --- | --- | --- | --- |
Measuring Internal Product Attributes    ◾    353
Spell-checker spec: The checker accepts as input a document file and an optional personal
dictionary file. The checker lists all words not contained in either of these files. The user can
query the number of words processed and the number of spelling errors found at any stage
during processing.
Errors-found enquiry
# Words-processed message
Words process enquiry
|     |     |     |     | Spelling | # Errors message |     |     |
| --- | --- | --- | --- | -------- | ---------------- | --- | --- |
User User
checker
Document file
Report on misspelt words
Personal dictionary
Words
Dictionary
A = # external inputs = 2,  B = # external outputs = 3,  C = # inquiries = 2,
D = # external files = 2, and  E = # internal files = 1
21
FIGURE 8.2  Computing basic function point components from specification.
multiplying the number of items in a variety by the weight of the variety
and summing over all 15:
15
∑
|     | UFC= | (Number of items of variety i) |     |     |     | ×(weight | )   |
| --- | ---- | ------------------------------ | --- | --- | --- | -------- | --- |
i
  i=1
EXAMPLE 8.12
Consider the spelling checker introduced in Example 8.11. If we assume that
the complexity for each item is average, then the UFC is
|     |     | UFC = 4A + 5B + 4C + 10D + 7E = 58 |     |     |     |     |     |
| --- | --- | ---------------------------------- | --- | --- | --- | --- | --- |
If instead we learn that the dictionary file and the misspelled word report
are considered complex, then
|     | UFC = 4A + (5× 2 + 7× 1) + 4C + 10D + 10E = 63 |     |     |     |     |     |     |
| --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- |

TABLE 8.2  Function Point Complexity Weights
| Item               |     | Simple |     | Weighting Factor Average |     |     | Complex |
| ------------------ | --- | ------ | --- | ------------------------ | --- | --- | ------- |
| External inputs    |     |        | 3   |                          | 4   |     | 6       |
| External outputs   |     |        | 4   |                          | 5   |     | 7       |
| External inquiries |     |        | 3   |                          | 4   |     | 6       |
| External files     |     |        | 7   |                          | 10  |     | 15      |
| Internal files     |     |        | 5   |                          | 7   |     | 10      |

|        |          | Function |     | points 1 |     |     |     |
| ------ | -------- | -------- | --- | -------- | --- | --- | --- |
| Number | of items |          |     |          |     |     |     |
A = External inputs (e.g. file names, menu selections) Measuring Internal Product Attributes    ◾    353
| B = External |     | outputs (e.g. reports and messages)  |     |     |     |     |     |
| ------------ | --- | ------------------------------------ | --- | --- | --- | --- | --- |
C = External inquiries (interactive inputs requiring a response)
Spell-checker spec: The checker accepts as input a document file and an optional personal
| D = External |     | files (interfaces to other |     |     | systems) |     |     |
| ------------ | --- | -------------------------- | --- | --- | -------- | --- | --- |
dictionary file. The checker lists all words not contained in either of these files. The user can
query the number of words processed and the number of spelling errors found at any stage
| E = Internal |     | files (master files in the system) |     |     |     |     |     |
| ------------ | --- | ---------------------------------- | --- | --- | --- | --- | --- |
during processing.
Errors-found enquiry
# Words-processed message
Example:
Words process enquiry
|     |     |     |     | Spelling | # Errors message |     |     |
| --- | --- | --- | --- | -------- | ---------------- | --- | --- |
User User
checker
Document file
Report on misspelt words
Personal dictionary
Words
Dictionary
A = # external inputs = 2,  B = # external outputs = 3,  C = # inquiries = 2,
D = # external files = 2, and  E = # internal files = 1
22
FIGURE 8.2  Computing basic function point components from specification.
multiplying the number of items in a variety by the weight of the variety
and summing over all 15:
15
∑
|     |     | UFC= | (Number of items of variety i) |     |     | ×(weight | )   |
| --- | --- | ---- | ------------------------------ | --- | --- | -------- | --- |
i
|     |     | i=1 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
EXAMPLE 8.12
Consider the spelling checker introduced in Example 8.11. If we assume that
the complexity for each item is average, then the UFC is
|     |     |     | UFC = 4A + 5B + 4C + 10D + 7E = 58 |     |     |     |     |
| --- | --- | --- | ---------------------------------- | --- | --- | --- | --- |
If instead we learn that the dictionary file and the misspelled word report
are considered complex, then
|     |     | UFC = 4A + (5× 2 + 7× 1) + 4C + 10D + 10E = 63 |     |     |     |     |     |
| --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- |

|     | TABLE 8.2          | Function Point Complexity Weights |        |                          |     |     |         |
| --- | ------------------ | --------------------------------- | ------ | ------------------------ | --- | --- | ------- |
|     | Item               |                                   | Simple | Weighting Factor Average |     |     | Complex |
|     | External inputs    |                                   | 3      |                          | 4   |     | 6       |
|     | External outputs   |                                   | 4      |                          | 5   |     | 7       |
|     | External inquiries |                                   | 3      |                          | 4   |     | 6       |
|     | External files     |                                   | 7      |                          | 10  |     | 15      |
|     | Internal files     |                                   | 5      |                          | 7   |     | 10      |

Measuring Internal Product Attributes    ◾    353
Spell-checker spec: The checker accepts as input a document file and an optional personal
dictionary file. The checker lists all words not contained in either of these files. The user can
query the number of words processed and the number of spelling errors found at any stage
during processing.
Errors-found enquiry
# Words-processed message
Words process enquiry
|     |     |     |     |     | Spelling | # Errors message |     |     |
| --- | --- | --- | --- | --- | -------- | ---------------- | --- | --- |
User User
checker
Document file
Report on misspelt words
Personal dictionary
Words
Dictionary
A = # external inputs = 2,  B = # external outputs = 3,  C = # inquiries = 2,
D = # external files = 2, and  E = # internal files = 1
FIGURE 8.2  Computing basic function point components from specification.
multiplying the number of items in a variety by the weight of the variety
and summing over all 15:
15
∑
|     |     | UFC= | (Number of items of variety i) |     |     |     | ×(weight | )   |
| --- | --- | ---- | ------------------------------ | --- | --- | --- | -------- | --- |
i
|     |     |     | i=1 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
EXAMPLE 8.12
Consider the spelling checker introduced in Example 8.11. If we assume that
the complexity for each item is average, then the UFC is
|     |                                                                              |     | UFC = 4A + 5B + 4C + 10D + 7E = 58 |     |     |          |     |     |
| --- | ---------------------------------------------------------------------------- | --- | ---------------------------------- | --- | --- | -------- | --- | --- |
|     | If instead we learn that the dictionary file and the misspelled word report  |     | Function                           |     |     | points 2 |     |     |
are considered complex, then
|     |     |     | UFC = 4A + (5× 2 + 7× 1) + 4C + 10D + 10E = 63 |     |     |     |     |     |
| --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- |

| Complexity                   |                    |     | for each                          |        | item => weight           |         |            |         |
| ---------------------------- | ------------------ | --- | --------------------------------- | ------ | ------------------------ | ------- | ---------- | ------- |
|                              | TABLE 8.2          |     | Function Point Complexity Weights |        |                          |         |            |         |
|                              | Item               |     |                                   | Simple | Weighting Factor Average |         |            | Complex |
|                              | External inputs    |     |                                   | 3      |                          | 4       |            | 6       |
|                              | External outputs   |     |                                   | 4      |                          | 5       |            | 7       |
|                              | External inquiries |     |                                   | 3      |                          | 4       |            | 6       |
|                              | External files     |     |                                   | 7      |                          | 10      |            | 15      |
|                              | Internal files     |     |                                   | 5      |                          | 7       |            | 10      |
| Unadjusted                   |                    |     | function                          |        | count:                   |         |            |         |
| UFC = ∑ (# item of type i) × |                    |     |                                   |        |                          | (weight | of type i) |         |
| Example: all average         |                    |     |                                   |        | complexity               |         |            |         |
A = 2, B = 3, C = 2, D = 2, E = 1
UFC = 4 A + 5 B + 4 C + 10 D + 7 E = 58
23

Function points 3
| 354    ◾    | Software Metrics                |                                               |         |         |                        |     |     |
| ----------- | ------------------------------- | --------------------------------------------- | ------- | ------- | ---------------------- | --- | --- |
| Technical   |                                 | complexity                                    |         | factors | (TCF)                  |     |     |
|             | TABLE 8.3                       | Components of the Technical Complexity Factor |         |         |                        |     |     |
|             | F  Reliable backup and recovery |                                               |         |         | F  Data communications |     |     |
|             | 1                               |                                               |         |         | 2                      |     |     |
|             | F  Distributed functions        |                                               |         |         | F  Performance         |     |     |
|             | 3                               |                                               |         |         | 4                      |     |     |
|             | F  Heavily used configuration   |                                               |         |         | F  Online data entry   |     |     |
|             | 5                               |                                               |         |         | 6                      |     |     |
|             | F  Operational ease             |                                               |         |         | F  Online update       |     |     |
|             | 7                               |                                               |         |         | 8                      |     |     |
|             | F  Complex interface            |                                               |         |         | F  Complex processing  |     |     |
|             | 9                               |                                               |         |         | 10                     |     |     |
|             | F  Reusability                  |                                               |         |         | F  Installation ease   |     |     |
|             | 11                              |                                               |         |         | 12                     |     |     |
|             | F  Multiple sites               |                                               |         |         | F  Facilitate change   |     |     |
|             | 13                              |                                               |         |         | 14                     |     |     |
| Each        | F between                       |                                               | 0 and 5 |         |                        |     |     |
To complete our computation of FPs, we calculate an adjusted function-
i
point count, FP, by multiplying UFC by a technical complexity factor, TCF.  TCF = 0.65 + 0.01 ∑ F
i
This factor involves the 14 contributing factors listed in Table 8.3.
|     | FP = UFC × |     | TCF |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- |
Each component or subfactor in Table 8.3 is rated from 0 to 5, where 0
means the subfactor is irrelevant, 3 means it is average, and 5 means it is
esEsexnatiaml top tlhee: s y6s tfeamc bteoinrgs bauitlt .0 A,l t6ho fuagch tthoersse iantte g3er,  r2at ifnagcs ftoormrs ana t 5
ordinal scale, the values are used as if they are a ratio scale, contrary to
|     | TCF = 0.65 + 0.01 (6 × |     |     | 3 + 2 × | 5) = 0.93 |     |     |
| --- | ---------------------- | --- | --- | ------- | --------- | --- | --- |
the principles we introduced in Chapter 2. Also, we find it curious that the
|     | FP = 58 × |     | 0.93 = 54 |     |     |     |     |
| --- | --------- | --- | --------- | --- | --- | --- | --- |
“average” value of 3 is not the median value.
The following formula combines the 14 ratings into a final technical
24
complexity factor:
14
∑
|     |     |     | TCF | = 0.65 + 0.01 | F   |     |     |
| --- | --- | --- | --- | ------------- | --- | --- | --- |
i
i=1

This factor varies from 0.65 (if each F is set to 0) to 1.35 (if each F is
|     |     |     |     | i   |     |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- |
set to 5). The final calculation of FPs multiplies the UFC by the technical
complexity factor:
|     |     |     | FP = UFC × TCF |     |     |     |     |
| --- | --- | --- | -------------- | --- | --- | --- | --- |
EXAMPLE 8.13
To continue our FP computation for the spelling checker in Example 8.11, we

evaluate the technical complexity factor. After having read the specification
in Figure 8.2, it seems reasonable to assume that F , F , F , F , F , and F
|     |     |     |     |     | 3 5 9 | 11 12 | 13  |
| --- | --- | --- | --- | --- | ----- | ----- | --- |
are 0, that F , F , F , F , F , and F  are 3, and that F  and F  are 5. Thus, we
|     | 1   | 2 6 | 7 8 | 14  | 4 10 |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- |
calculate the TCF as
|     |     |     | TCF = 0.65 + 0.01(18 + 10) = 0.93 |     |     |     |     |
| --- | --- | --- | --------------------------------- | --- | --- | --- | --- |
Since UFC is 63, then
|     |     |     | FP = 63 × 0.93 = 59 |     |     |     |     |
| --- | --- | --- | ------------------- | --- | --- | --- | --- |

|                | Function          |     | points: issues |     |     |
| -------------- | ----------------- | --- | -------------- | --- | --- |
| • Subjectivity | in the technology |     | factor         |     |     |
May range from 0.65 to 1.35 = ±35%
| • Problems                   | with double counting  |           |                    |     |      |
| ---------------------------- | --------------------- | --------- | ------------------ | --- | ---- |
| e.g. in weighting            | + in technology       |           | factors            |     |      |
| • Problems                   | with counterintuitive |           | values             |     |      |
| For instance, all Fi average |                       | (3) gives | TCF = 1.07 instead |     | of 1 |
| • Problems                   | with accuracy         |           |                    |     |      |
TCF does not significantly improve resource estimation, UFC as good as FP
| • Problems | with changing | requirements |     |     |     |
| ---------- | ------------- | ------------ | --- | --- | --- |
FP increases as project progresses, number and complexity of items increases
| • Problems | with differentiating |     | specified | items |     |
| ---------- | -------------------- | --- | --------- | ----- | --- |
Subjectivity in evaluating the input items and technology factor components.
| • Problems | with subjective weighting |     |     |     |     |
| ---------- | ------------------------- | --- | --- | --- | --- |
Values may not be appropriate in all development environments
| • Problems | with measurement |     | theory |     |     |
| ---------- | ---------------- | --- | ------ | --- | --- |
The calculation combines measures from different scales in a manner that is
| inconsistent | with measurement |     | theory |     |     |
| ------------ | ---------------- | --- | ------ | --- | --- |
25

Measuring Internal Product Attributes   ◾   359
|     |     |     | TABLE 8.4                        |     | C2 Object Point Complexity Levels |     |     |     |                                  |             |     |     |     |
| --- | --- | --- | -------------------------------- | --- | --------------------------------- | --- | --- | --- | -------------------------------- | ----------- | --- | --- | --- |
|     |     |     |                                  |     | For Screens                       |     |     |     |                                  | For Reports |     |     |     |
|     |     |     | Number and Source of Data Tables |     |                                   |     |     |     | Number and Source of Data Tables |             |     |     |     |
Number of  Total  Total <8  Total  Number of  Total <4  Total <8  Total 8+
|     |     |     | views     |     | <4 (<2   | (2–3     | 8+ (>3   | sections  |     | (<2      | (2–3     |     | (>3      |
| --- | --- | --- | --------- | --- | -------- | -------- | -------- | --------- | --- | -------- | -------- | --- | -------- |
|     |     |     | contained |     | server,  |          | server,  | contained |     |          |          |     |          |
|     |     |     |           |     |          | server,  |          |           |     | server,  | server,  |     | server,  |
|     |     |     |           |     | <2       | 3–5      | >5       |           |     | <2       | 3–5      |     | >5       |
|     |     |     |           |     | client)  | client)  | client)  |           |     | client)  | client)  |     | client)  |
<3
|     |     |     |     |     | Simple | Simple    | Medium    | 0 or 1 |     | Simple | Simple    |     | Medium    |
| --- | --- | --- | --- | --- | ------ | --------- | --------- | ------ | --- | ------ | --------- | --- | --------- |
|     |     |     | 3–7 |     | Simple | Medium    | Difficult | 2 or 3 |     | Simple | Medium    |     | Difficult |
|     |     |     | 8+  |     | Medium | Difficult | Difficult | 4+     |     | Medium | Difficult |     | Difficult |
Source:  Boehm B.W. et al. Software Cost Estimation with Cocomo II, Prentice-Hall, Upper
Saddle River, New Jersey, 2000.
application generates an initial size measure. It is assumed that these entities
COCOMO II
are defined in a standard way as part of an integrated software development
environment. Next, each entity is classified as simple, medium, or difficult,
much as are FPs. Table 8.4 contains guidelines for this classification.
COCOMO II (Boehm et al.) The number in each cell is weighted according to Table 8.5. The weights
reflect the relative effort required to implement an instance of that com-
| Fully | specified |     |     | system => function |     |     |     | points |     |     |     |     |     |
| ----- | --------- | --- | --- | ------------------ | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
plexity level.
| Early | development |     |     |     | => C2 ("object") points |     |     |     |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
As with FPs, the weighted instances are summed to yield a single C2
|     |     |     |     |     |     |     | Measuring Internal Product Attributes  |     |     |     |     |     |   ◾    359   |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | ------------ |
object point number. Then, the procedure differs from FPs in that reuse is
|     | count number |     |     |     | of screens, reports, components |     |     |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
taken into account, since the C2 object points are intended for use in effort
|     | apply |            | complexity                                                                |     | weights                           |     |     |     |     |     |     |     |     |
| --- | ----- | ---------- | ------------------------------------------------------------------------- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |       | TABLE 8.4  | estimation. Assuming that r% of the objects will be reused from previous  |     | C2 Object Point Complexity Levels |     |     |     |     |     |     |     |     |
projects, the number of new object points is calculated to be
|     |     |     |     |     | For Screens |     |     |     |     | For Reports |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | ----------- | --- | --- | --- |
Number and Source of Data Tables Number and Source of Data Tables
|     |     |     |     |     | New object points = (Object points) × (100 − r)/100 |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Number of  Total  Total <8  Total  Number of  Total <4  Total <8  Total 8+
|     |     | views  |     |     | <4 (<2  | (2–3  | 8+ (>3  | sections  |     | (<2  |     | (2–3  | (>3  |
| --- | --- | ------ | --- | --- | ------- | ----- | ------- | --------- | --- | ---- | --- | ----- | ---- |
To use this number for effort estimation, COCOMO II determines a
contained server,  server,  server,  contained server,  server,  server,
productivity rate (i.e., new object points per person-month) from a table
|     |     |     |     |     | <2  | 3–5  | >5  |     |     | <2  |     | 3–5  | >5  |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ---- | --- |
based on developer experience and capability, coupled with ICASE matu- client) client) client) client) client) client)

<3 rity and capability. Simple Simple Medium 0 or 1 Simple Simple Medium
|     |     | 3–7 |     |     | Simple | Medium    | Difficult | 2 or 3 |     | Simple | Medium    |     | Difficult |
| --- | --- | --- | --- | --- | ------ | --------- | --------- | ------ | --- | ------ | --------- | --- | --------- |
|     |     | 8+  |     |     | Medium | Difficult | Difficult | 4+     |     | Medium | Difficult |     | Difficult |
TABLE 8.5
Complexity Weights for Object Points
Source:  Boehm B.W. et al. Software Cost Estimation with Cocomo II, Prentice-Hall, Upper
|     |     |     |     |     | Object Type |     | Simple |     | Medium |     | Difficult |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | ------ | --- | ------ | --- | --------- | --- | --- |
Saddle River, New Jersey, 2000.
|     |     |                                                                                   |     |     | Screen        |     | 1   |     |     | 2   |     | 3   |     |
| --- | --- | --------------------------------------------------------------------------------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |                                                                                   |     |     | Report        |     | 2   |     |     | 5   |     | 8   |     |
|     |     | application generates an initial size measure. It is assumed that these entities  |     |     | 3GL component |     | –   |     |     | –   |     | 10  |     |
26
are defined in a standard way as part of an integrated software development
environment. Next, each entity is classified as simple, medium, or difficult,
much as are FPs. Table 8.4 contains guidelines for this classification.
The number in each cell is weighted according to Table 8.5. The weights
reflect the relative effort required to implement an instance of that com-
plexity level.
As with FPs, the weighted instances are summed to yield a single C2
object point number. Then, the procedure differs from FPs in that reuse is
taken into account, since the C2 object points are intended for use in effort
estimation. Assuming that r% of the objects will be reused from previous
projects, the number of new object points is calculated to be
|     |     |     |     |     | New object points = (Object points) × (100 − r)/100 |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
To use this number for effort estimation, COCOMO II determines a
productivity rate (i.e., new object points per person-month) from a table
  based on developer experience and capability, coupled with ICASE matu-
rity and capability.
TABLE 8.5
Complexity Weights for Object Points
|     |     |     |     | Object Type   |     |     | Simple |     | Medium |     |     | Difficult |     |
| --- | --- | --- | --- | ------------- | --- | --- | ------ | --- | ------ | --- | --- | --------- | --- |
|     |     |     |     | Screen        |     |     | 1      |     |        | 2   |     | 3         |     |
|     |     |     |     | Report        |     |     | 2      |     |        | 5   |     | 8         |     |
|     |     |     |     | 3GL component |     |     | –      |     |        | –   |     | 10        |     |

PRODUCT METRICS: STRUCTURE
27

Structure measurement
| Product size           | does | not tell everything |                |        |
| ---------------------- | ---- | ------------------- | -------------- | ------ |
| Product structure      |      | also                | plays          | a role |
| Capture the complexity |      |                     | of the product |        |
Applicable to design, code, seen as a graph
Two perspectives:
• Control flow
• Data flow
28

|         | Overall   |                                  | complexity              |                     | measure? |
| ------- | --------- | -------------------------------- | ----------------------- | ------------------- | -------- |
| We      | would     | like                             | to have a comprehensive |                     |          |
| measure |           | of overall                       |                         | software complexity |          |
|         | Indicates | comprehensibility, correctness,  |                         |                     |          |
maintainability, reliability, testability, ease of
implementation, …
| This does |             | not exist! |     |     |     |
| --------- | ----------- | ---------- | --- | --- | --- |
|           | Conflicting | goals      |     |     |     |
29

Structural attributes
• Complexity
complicatedness of the connections between elements in a system
model
positive, monotonic, additive on disjoint elements
•
Length
| distances between | elements |     |     |     |
| ----------------- | -------- | --- | --- | --- |
positive, monotonic, max on disjoint elements
• Coupling
| links to/from                | elements | outside | the module    |         |
| ---------------------------- | -------- | ------- | ------------- | ------- |
| positive, monotonic, at most |          |         | sum on merged | modules |
• Cohesion
| connections between        |     | internal | elements  |         |
| -------------------------- | --- | -------- | --------- | ------- |
| 0 to 1, monotonic, at most |     | sum      | on merged | modules |
30

376 ◾ Software Metrics
measure would indicate the difference between (1) a specific graph repre-
sentation modeling some aspects of software and (2) a tree structure. We
will also see that one can define measures based on the occurrences of
realizations of design structures such as design patterns.
We now examine the measurement of the internal structure of software
starting from the perspective of the control flow in individual program
units.
9.2 CONTROL FLOW STRUCTURE OF PROGRAM UNITS
A great deal of early software metrics work was devoted to measuring
the control flow structure of individual functions, procedures, or meth-
ods implemented as imperative language programs or algorithms. This
work is still relevant, especially when applied to problems in software test-
ing. The control flow measures are usually modeled with directed graphs,
where each node (or point) corresponds to a program statement or basic
block (code that always executes sequentially), and each arc (or directed
edge) indicates the flow of control from one statement or basic block to
another. We call these directed graphs control flowgraphs or flowgraphs.
Figure 9.1 presents a simple example of a program, A, and a reasonable
interpretation of its corresponding flowgraph, F(A). We say “reasonable
interpretation” because it is not always obvious how to map a program A
to a flowgraph F(A). The flowgraph is a good model for defining measures
of control flow structure, because it makes explicit many of the structural
properties of the program. The nodes enumerate the program statements,
and the arcs make visible the control patterns.
Control flow graph
10
10 INPUT P 20
20 Div = 2
30 Lim = INT(SQR(P))
30
40 Flag = P/Div - INT(P/Div)
50 IF Flag = 0 OR Div = Lim THEN 80
40
60 Div = Div + 1
70 GO TO 40
50
80 IF Flag <>0 OR P>4 THEN 110
90 PRINT Div; ‘‘Smallest factor of’’; P; ‘‘.’’ t f
80
60 100 GO TO 120 t
f
110 PRINT P; ‘‘ is prime’’
110 90
120 END
120
A graph with distinguished start and stop nodes
We want measures that are independent of a particular
FIGURE 9.1 A program and its corresponding flowgraph.
view (granularity) of the graph
31
376 ◾ Software Metrics
measure would indicate the difference between (1) a specific graph repre-
sentation modeling some aspects of software and (2) a tree structure. We
will also see that one can define measures based on the occurrences of
realizations of design structures such as design patterns.
We now examine the measurement of the internal structure of software
starting from the perspective of the control flow in individual program
units.
9.2 CONTROL FLOW STRUCTURE OF PROGRAM UNITS
A great deal of early software metrics work was devoted to measuring
the control flow structure of individual functions, procedures, or meth-
ods implemented as imperative language programs or algorithms. This
work is still relevant, especially when applied to problems in software test-
ing. The control flow measures are usually modeled with directed graphs,
where each node (or point) corresponds to a program statement or basic
block (code that always executes sequentially), and each arc (or directed
edge) indicates the flow of control from one statement or basic block to
another. We call these directed graphs control flowgraphs or flowgraphs.
Figure 9.1 presents a simple example of a program, A, and a reasonable
interpretation of its corresponding flowgraph, F(A). We say “reasonable
interpretation” because it is not always obvious how to map a program A
to a flowgraph F(A). The flowgraph is a good model for defining measures
of control flow structure, because it makes explicit many of the structural
properties of the program. The nodes enumerate the program statements,
and the arcs make visible the control patterns.
10
10 INPUT P 20
20 Div = 2
30 Lim = INT(SQR(P))
30
40 Flag = P/Div - INT(P/Div)
50 IF Flag = 0 OR Div = Lim THEN 80
40
60 Div = Div + 1
70 GO TO 40
50
80 IF Flag <>0 OR P>4 THEN 110
90 PRINT Div; ‘‘Smallest factor of’’; P; ‘‘.’’ 80 t f
60
100 GO TO 120 t
f
110 PRINT P; ‘‘ is prime’’
110 90
120 END
120
FIGURE 9.1 A program and its corresponding flowgraph.

380   ◾   Software Metrics
D (A,X) (meaning D  with parameters A and X) is an explicit denotation
|     | 2   |     |     |     | 2   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of the construct while A do X. Sometimes, for convenience, we refer only
to the unparameterized names like D , meaning the generic while–do con-
2
trol construct.
Most imperative programs have built-in control constructs for the flow-
graphs in Figure 9.2, but the same is not true for the control constructs
shown in Figure 9.3. (We shall soon see that the reasons for this difference
are more dogmatic than rational.) In theory, each of these additional con-
structs can be implemented using goto statements (which are available in
C or C++, but not in many languages such as Java or Python). For example,
|     |                               | Flowgraph |     |     |     |                                         |     | structures |     |     |     |     |     |
| --- | ----------------------------- | --------- | --- | --- | --- | --------------------------------------- | --- | ---------- | --- | --- | --- | --- | --- |
|     | the two-exit loop construct L |           |     |     |     |  is equivalent to the following C code: |     |            |     |     |     |     |     |
Measuring Internal Product Attributes   ◾   379   2
loop:
,…,X
|     | X;               |     | X   | X   |        |     | X   |     | P  or P | (X ,X |     | )   |     |
| --- | ---------------- | --- | --- | --- | ------ | --- | --- | --- | ------- | ----- | --- | --- | --- |
|     |                  |     | 1   | 2   |        |     | n   |     | n n     | 1     | 2   | n   |     |
|     | if (A) goto end; |     |     |     | ...... |     |     |     |         |       |     |     |     |
X1;X2;…;Xn
Y;
if (B) goto end;
|     |                 |     |         |        |     |     |     |             |         |     | C  or C | (A,X    | ,…,X ) |
| --- | --------------- | --- | ------- | ------ | --- | --- | --- | ----------- | ------- | --- | ------- | ------- | ------ |
|     |                 |     |         |        |     | A   |     |             |         |     | n       | n       | 1 n    |
|     | else goto loop; | A   | D  or D | (A,X)  |     |     |     |             |         |     |         |         |        |
|     | t               |     | 0       | 0      |     |     |     |             |         |     |         |         | A      |
|     |                 |     |         |        | t   |     | f   | D  or D     | (A,X,Y) |     |         |         |        |
|     | end: return;    |     | If A t  | h en X |     |     |     | 1           | 1       |     | a       |         |        |
| X   |                 |     |         |        |     |     |     |             |         |     | X       | 1       | a      |
|     |                 | f   |         |        | X   |     | Y   |             |         |     | 1       | a       | n X    |
|     |                 |     |         |        |     |     |     |             |         |     |         | 2       | n      |
|     |                 |     |         |        |     |     |     | If A then X |         |     | X       |         |        |
|     |                 |     |         |        |     |     |     |             |         |     |         | 2 ..... |        |
         else Y
Although we can construct the flowgraphs in Figures 9.2 and 9.3 using
the goto construct, most developers avoid the goto construct because it
|     |     | A   |     |     |     |     |     | X   |     |     |     | case A of |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- |
   a   :  X
|     | allows you to create very complex control flow that is difficult to under-  |     | D  or D      | (A,X) |     |     |     |                  |             |     |     | 1             | 1   |
| --- | --------------------------------------------------------------------------- | --- | ------------ | ----- | --- | --- | --- | ---------------- | ----------- | --- | --- | ------------- | --- |
|     | f                                                                           |     | 2            | 2     |     |     |     | D                |  or D (A,X) |     |     |    a  :  X    |     |
|     |                                                                             |     |              |       |     |     |     |                  | 3 3         |     |     | 2             | 2   |
|     |                                                                             | t   | while A do X |       |     |     |     | repeat X until A |             |     |     |         . ... |     |
|     | stand, debug, and modify. Experience suggests that it is best to build the  |     |              |       |     |     |     | f                |             |     |     |               |     |
   a   :  X
|     |     |     |     |     |     |     |     |     |     |     |     | n   | n   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
control flow of procedures, functions, and methods using only the control
A
|     | X   |     |     |     |     | t   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
flow constructs that implement those modeled in Figure 9.2 and possibly
| FIGURE 9.2  |     |     | Common flowgraphs from program structure models. |     |     |     |     |     |     |     |     |     |     |
| ----------- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
X
X
A
f
that correspond to the basic control constructs in imperative language
B
t
|              |     |     |     |     |     | A   |     | B   |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| programming. |     |     | f   |     |     |     | f   |     |     |     |     |     |     |
f
t
|     | For example, the P | Y   |     | X   |  flowgraph* represents the construct sequence, where  | t   |     | t   |     |     |     | A   |     |
| --- | ------------------ | --- | --- | --- | ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |                    |     |     | 2   |                                                       |     |     |     |     |     | t   |     |     |
f
a program consists of a sequence of two statements. Beneath the name of

Y
each construct in Figure 9.2, we have written an example of program code
| for that construct. For instance, the example code for the D |     | D or D | (A,B,X,Y) |     |     | L   | or L | (A,B,X,Y) |     |     | D   | or D  construct  (A,X,Y) |     |
| ------------------------------------------------------------ | --- | ------ | --------- | --- | --- | --- | ---- | --------- | --- | --- | --- | ------------------------ | --- |
|                                                              |     | 5      | 5         |     |     | 2   |      | 2         |     |     | 4   | 4                        |     |
0
is the if–then statement. Not all imperative languages have built-in con-
|     |     | “lazy Boolean evaluation OR” |     |     |     | “two-exit loop” |     |     |     |     | “middle-exit loop” |     |     |
| --- | --- | ---------------------------- | --- | --- | --- | --------------- | --- | --- | --- | --- | ------------------ | --- | --- |
32
| structs for each of the control constructs shown here, nor is the particular  |     | If (A or B) then X else Y    |     |     |     | loop                            |     |     |     |     | loop               |     |     |
| ----------------------------------------------------------------------------- | --- | ---------------------------- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------------------ | --- | --- |
|                                                                               |     | in Turbo Pascal with Boolean |     |     |     |   X: exit when A; Y exit when B |     |     |     |     |   X; exit when A;Y |     |     |
code for the constructs unique.
|     |     | evaluation set to LAZY |     |     |     | loop end |     |     |     |     | loop end |     |     |
| --- | --- | ---------------------- | --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- |
If A or else B then X else Y
|     |     | in Ada |     |     |     |     | in Ada |     |     |     | in Ada |     |     |
| --- | --- | ------ | --- | --- | --- | --- | ------ | --- | --- | --- | ------ | --- | --- |
EXAMPLE 9.3
|     | FIGURE 9.3  |     | Flowgraphs for less common control constructs. |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 9.2 contains an example of the repeat–until statement. An alternate
expression for that construct is
10 X
If A then goto 20 else goto 10
20 end

|     | The flowgraph model for this program is identical to D |     |     |     |     |     |     |     |     |     |  in Figure 9.2. |     |     |
| --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- |
3
|     | Strictly  |     | speaking,  |     | a  flowgraph  |     | is  | “parameterized”  |     |     | when  | we  | associ- |
| --- | --------- | --- | ---------- | --- | ------------- | --- | --- | ---------------- | --- | --- | ----- | --- | ------- |
ate with it the actual code that it represents. For example, the notation
* The sequence statement P  is a special case of a sequence of n statements P . Another special
|     |               |     |                                                                                  | 2   |     |     |     |     |     |     |     | n   |     |
| --- | ------------- | --- | -------------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | instance of P |     |  is the case n = 1, which represents a program consisting of a single statement. |     |     |     |     |     |     |     |     |     |     |
n

|     |     |     |     |     |     |     |     | Measuring Internal Product Attributes  |     |     |     |     |   ◾    381   |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | ------------ |
Figure 9.3, as provided in an implementation language. There are many
possible variations of the constructs in Figure 9.3. For example, a variation
in D  is the if–and–then–else construct, as well as more complex condi-
5
|     |     |     | 382    ◾    | Software Metrics |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tions like
way. Suppose A and A′ are two blocks of program code, and recall that, in    if (A or B or C) then X else Y,  if ((A or B) and (B or C))
general, the flowgraph model of a program A is denoted by F(A). Then
However, all of the flowgraphs in Figures 9.2 and 9.3 have an impor-
|     |     |     | tant common property that makes them suitable as “building blocks” for  |     |     |     | F(A; A′) = F(A); F(A′) |     |     |     |     |     |     |
| --- | --- | --- | ----------------------------------------------------------------------- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- |

structured program units. To understand it, we must define formally the
ways that we can build flowgraphs. Thus, the flowgraph of the program sequence is equal to the sequence
of the flowgraphs.
9.2.1.1  Let F Sequencing and Nesting  and F  be two flowgraphs. Suppose F  has a procedure node x. Then
|     |     |     |     | 1   | 2   |     |     |     |     | 1   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the nesting of F There are just two legitimate operations we can use to build new flow-  onto F  at x is the flowgraph formed from F  by replacing
|     |     |     |     |     | 2   | 1   |     |     |     |     |     | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the arc from x with the whole of F . The resulting flowgraph is written as
graphs from old: sequencing and nesting. Both have a natural interpreta-
2
tion in terms of program structure.
|     |     |     |     |     |     |     |     | F  (F |  on x) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------ | --- | --- | --- | --- |
Let F  and F  be two flowgraphs. Then the sequence of F  and F  is the
|     |     |     |     | 1   | 2   |     |     | 1   | 2   |     |     | 1   | 2   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
flowgraph formed by merging the stop node of F  with the start node of F .
1 2
Alternatively,  we  write  F (F )  when  there  is  no  ambiguity  about  the
|     |     |     | The resulting flowgraph is written as |     |     |     | 1   | 2   |     |     |     |     |     |
| --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
node onto which the graph is nested.
|     |     |     |     |     |     | F ; F |  or Seq (F |     | , F ) or P |  (F | , F ) |     |     |
| --- | --- | --- | --- | --- | --- | ----- | ---------- | --- | ---------- | --- | ----- | --- | --- |
|     |     |     |     |     |     | 1     | 2          | 1   | 2          | 2 1 | 2     |     |     |
EXAMPLE 9.5
EXAMPLE 9.4
Figure 9.5 shows the result of nesting the D  flowgraph onto the D  flowgraph.
|     |     |     |     |     |     |     |     |     | 3   |     |     | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure  9.4  shows  the  result  of  forming  the  sequence  of  the  D   and  D
|     |     |     |     |     |     |     |     |     |     |     |     | 1   | 3   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
flowgraphs.
|     |     | Sequencing | EXAMPLE 9.6 |     |     | and nesting |     |     |     |     |     |     |     |
| --- | --- | ---------- | ----------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
The flowgraph sequence operation corresponds to the sequence operation
Figure 9.6 shows the construction of a flowgraph from a number of nesting
(also called concatenation) in imperative language programming. In fact,
and sequence operations.
the flowgraph operation preserves the program operation in the following
| Two | legitimate | operations |     |     | to build | new flowgraphs: |     |     |     |     |     |     |     |
| --- | ---------- | ---------- | --- | --- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- |

The flowgraph nesting operation corresponds to the operation of proce-
|     |          |     |     |     |     |     |     |     |     | D   | ; D |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |          |     |     |     |     |     |     | D   |     |     | 1 3 |     |     |
| •   |          |     |     |     |     |     |     | 3   |     |     |     |     |     |
|     | Sequence | F   | ; F |     | D   |     |     |     |     |     |     |     |     |
1
|     |     | 1   | dure substitution in imperative language programming. Specifically, con- 2 |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | -------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sider a program A in which the procedure A′ is called by a parameter x.
Sequence
Then
|     |     |     |     |     | F(A with A′ substituted for x) = F(A) (F(A′) on x) |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |

| •   | Nesting | F [F | on x]       |     |                                  |     |     |     |     |       |        |     |     |
| --- | ------- | ---- | ----------- | --- | -------------------------------- | --- | --- | --- | --- | ----- | ------ | --- | --- |
|     |         | 1 2  |             |     |                                  |     |     |     |     |       |        |     |     |
|     |         |      |             |     |                                  |     |     |     |     | D  (D |  on x) |     |     |
|     |         |      |             |     |                                  |     | D   |     |     | 1     | 3      |     |     |
|     |         |      | FIGURE 9.4  |     | Applying the sequence operation. |     | 3   |     |     |       |        |     |     |
D
1
X
Nested
With
on x
| Prime flowgraph |                        |        | =           |                 |                                 |               |     |     |            |     |     |     |     |
| --------------- | ---------------------- | ------ | ----------- | --------------- | ------------------------------- | ------------- | --- | --- | ---------- | --- | --- | --- | --- |
| a graph  that   |                        | cannot | be          | composed        |                                 | by sequencing |     |     | or nesting |     |     |     |     |
|                 |                        |        | FIGURE 9.5  |                 | Applying the nesting operation. |               |     |     |            |     |     |     |     |
|                 | All graphs of previous |        |             | slide are prime |                                 |               |     |     |            |     |     |     |     |
33

Structured flowgraphs
| Given           | a family | S of prime flowgraphs, |               |        |               |     |
| --------------- | -------- | ---------------------- | ------------- | ------ | ------------- | --- |
| a flow graph is |          | S-structured           |               | iff    |               |     |
| it is generated |          | from                   | S by a finite | number | of sequencing |     |
and nesting
all graphs in S are S-structured
|                 |     |     | Measuring Internal Product Attributes  |     |     |   ◾    385   |
| --------------- | --- | --- | -------------------------------------- | --- | --- | ------------ |
| Example: S = {D |     | , D | }                                      |     |     |              |
|                 |     | 1   | 2                                      |     |     |              |
D
|     | 1   |     | D   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
2
X
D (D )
1 2
D ;D
1 2
|     |     |     |     |        | D ;D ; (D | (D ))  |
| --- | --- | --- | --- | ------ | --------- | ------ |
|     |     |     |     | D (D ) | 1 2       | 2 1    |
2 1
34
etc.
|     | FIGURE 9.7  | Examples of S-structured graphs when S = {D |     |     | , D }. |     |
| --- | ----------- | ------------------------------------------- | --- | --- | ------ | --- |
1 2
EXAMPLE 9.9
For  S = {D ,  D },  Figure  9.7  shows  the  examples  of  various  S-structured
1 2
graphs.
The definition allows us to nominate, for any particular development
environment, a set of legal control structures (represented by the basic
S-graphs) suited for particular applications. Then, by definition, any con-
trol structure composed from this nominated set will be “structured” in
terms of this local standard; in other words, the set derived from the basic
S-graphs will be S-structured.
EXAMPLE 9.10
Let SD = {P , D , D }. Then the class of SD-graphs is the class of flowgraphs com-
1 0 2
monly called (in the literature of structured programming) the D-structured
(or sometimes just structured) graphs. Stated formally, the Böhm and Jacopini

result asserts that every algorithm can be encoded as an SD-graph. Although
SD is sufficient in this respect, it is normally extended to include the structures
|     | D  (if–then–else) and D |     |  (repeat–until). |     |     |     |
| --- | ----------------------- | --- | ---------------- | --- | --- | --- |
|     | 1                       |     | 3                |     |     |     |
For reasons that have been discussed extensively elsewhere, it is now
common to accept a larger set than SD as the basis for structured program-
ming. For example, there are very powerful arguments for including all
of the primes in Figure 9.3. Many modern languages have constructs that

380   ◾   Software Metrics
D (A,X) (meaning D  with parameters A and X) is an explicit denotation
|     |     | 2   |     |     |     | 2   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of the construct while A do X. Sometimes, for convenience, we refer only
to the unparameterized names like D , meaning the generic while–do con-
2
trol construct.
Most imperative programs have built-in control constructs for the flow-
graphs in Figure 9.2, but the same is not true for the control constructs
shown in Figure 9.3. (We shall soon see that the reasons for this difference
are more dogmatic than rational.) In theory, each of these additional con-
|     |     |     | Structured |     |     |     |     |     |     | programs |     |     |     |     |     |     |
| --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
structs can be implemented using goto statements (which are available in
C or C++, but not in many languages such as Java or Python). For example,
|              |     | the two-exit loop construct L |                  |     |     |     |     |  is equivalent to the following C code: |     |       |     |     |     |     |     |     |
| ------------ | --- | ----------------------------- | ---------------- | --- | --- | --- | --- | --------------------------------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
| D-structured |     |                               | programs: S = {P |     |     |     |     | , D                                     |     | , D } |     |     |     |     |     |     |
2
|     |     |       |     |     |     |     |     | 1                                                 | 0   | 2   |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | loop: |     |     |     |     |     | Measuring Internal Product Attributes   ◾   379   |     |     |     |     |     |     |     |     |
Structured programs: S = {P , D , D , D , D , D , C (for all n), L }
|     |     |     |     |     |     |     | 1   |     | 0   | 1 2 | 3   |     | 4   | n   |     | 2   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
X;
if (A) goto end;
,…,X
|     |     |     |     | X   | X   |     |        | X   |     | P  or P    | (X   | ,X  | )   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | ---------- | ---- | --- | --- | --- | --- | --- |
|     |     | Y;  |     | 1   | 2   |     |        |     | n   | n          | n  1 | 2   | n   |     |     |     |
|     |     |     |     |     |     |     | ...... |     |     | X1;X2;…;Xn |      |     |     |     |     |     |
if (B) goto end;
else goto loop;
|     |     | end: return;                                                             |     |         |        |     |     |     |     |                 |     | C  or C | (A,X | ,…,X  | )   |     |
| --- | --- | ------------------------------------------------------------------------ | --- | ------- | ------ | --- | --- | --- | --- | --------------- | --- | ------- | ---- | ----- | --- | --- |
|     |     |                                                                          |     |         |        |     |     | A   |     |                 |     | n       | n    | 1     | n   |     |
|     |     |                                                                          | A   | D  or D | (A,X)  |     |     |     |     |                 |     |         |      |       |     |     |
|     |     | t                                                                        |     | 0       | 0      |     |     |     |     |                 |     |         |      | A     |     |     |
|     |     |                                                                          |     |         |        |     | t   | f   | D   |  or D (A,X,Y)   |     |         | a    |       |     |     |
|     | X   |                                                                          |     | If A t  | h en X |     |     |     |     | 1 1             |     |         | 1    |       |     |     |
|     |     |                                                                          |     |         |        |     |     |     |     |                 |     | X       |      | a     | a   |     |
|     |     |                                                                          | f   |         |        | X   |     |     | Y   |                 |     | 1       |      | 2     | n X |     |
|     |     | Although we can construct the flowgraphs in Figures 9.2 and 9.3 using    |     |         |        |     |     |     |     |                 |     |         | X    |       | n   |     |
|     |     |                                                                          |     |         |        |     |     |     |     | If A then X     |     |         | 2    | ..... |     |     |
|     |     | the goto construct, most developers avoid the goto construct because it  |     |         |        |     |     |     |     |          else Y |     |         |      |       |     |     |
allows you to create very complex control flow that is difficult to under-
|     |     |     | A   |     |     |     |     |     | X   |     |     |     | case A of |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- |
stand, debug, and modify. Experience suggests that it is best to build the
|     |     |                                                                            |     |              |       |     |     |     |     |                    |       |     |    a   |   :  X |     |     |
| --- | --- | -------------------------------------------------------------------------- | --- | ------------ | ----- | --- | --- | --- | --- | ------------------ | ----- | --- | ------ | ------ | --- | --- |
|     |     |                                                                            |     | D  or D      | (A,X) |     |     |     |     | D  or D            | (A,X) |     |        | 1 1    |     |     |
|     |     | f                                                                          |     | 2            | 2     |     |     |     |     | 3 3                |       |     |    a   |  :  X  |     |     |
|     |     | control flow of procedures, functions, and methods using only the control  |     |              |       |     |     |     |     |                    |       |     |        | 2   2  |     |     |
|     |     |                                                                            | t   | while A do X |       |     |     |     |     | f repeat X until A |       |     |        |  . ... |     |     |
|     |     |                                                                            |     |              |       |     |     |     |     |                    |       |     |    a   |   :  X |     |     |
|     |     | flow constructs that implement those modeled in Figure 9.2 and possibly    |     |              |       |     |     |     |     |                    |       |     |        | n n    |     |     |
A
|     |     |     | X   |     |     |     |     | t   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
X
|     |     |     |     |     | A   |     |     |     | X   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
f
|     | FIGURE 9.2  |     |     | Common flowgraphs from program structure models. |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
B
|     |     |     |     |     | t   |     |     |     |     | B   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | f   |     |     |     | A f |     |     |     |     |     |     |     |     |
f
|     | that correspond to the basic control constructs in imperative language  |     |     | t   |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |                                                                         |     | Y   |     | X   |     |     | t   |     | t   |     |     |     | A   |     |     |
t
programming.
f
For example, the P  flowgraph* represents the construct sequence, where
|     |     |     |     |     | 2   |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Y
a program consists of a sequence of two statements. Beneath the name of
|     |     |     | D or D | (A,B,X,Y) |     |     |     | L or L | (A,B,X,Y) |     |     |     | D or D | (A,X,Y) |     |     |
| --- | --- | --- | ------ | --------- | --- | --- | --- | ------ | --------- | --- | --- | --- | ------ | ------- | --- | --- |
|     |     |     | 5      | 5         |     |     |     | 2      | 2         |     |     |     | 4      | 4       |     |     |
each construct in Figure 9.2, we have written an example of program code
35
|     |     |     | “lazy Boolean evaluation OR” |     |     |     |     | “two-exit loop” |     |     |     |     | “middle-exit loop” |     |     |     |
| --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | ------------------ | --- | --- | --- |
for that construct. For instance, the example code for the D  construct
0
|     |     |     | If (A or B) then X else Y |     |     |     |     | loop |     |     |     |     | loop |     |     |     |
| --- | --- | --- | ------------------------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- | --- | --- | --- |
is the if–then statement. Not all imperative languages have built-in con-
|     |                                                                               |     | in Turbo Pascal with Boolean |     |     |     |     |   X: exit when A; Y exit when B |     |     |     |     |   X; exit when A;Y |     |     |     |
| --- | ----------------------------------------------------------------------------- | --- | ---------------------------- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------------------ | --- | --- | --- |
|     | structs for each of the control constructs shown here, nor is the particular  |     | evaluation set to LAZY       |     |     |     |     | loop end                        |     |     |     |     | loop end           |     |     |     |
If A or else B then X else Y
|     | code for the constructs unique. |             | in Ada |                                                |     |     |     |     | in Ada |     |     |     | in Ada |     |     |     |
| --- | ------------------------------- | ----------- | ------ | ---------------------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | ------ | --- | --- | --- |
|     |                                 | FIGURE 9.3  |        | Flowgraphs for less common control constructs. |     |     |     |     |        |     |     |     |        |     |     |     |
EXAMPLE 9.3
Figure 9.2 contains an example of the repeat–until statement. An alternate
expression for that construct is
10 X
If A then goto 20 else goto 10
20 end

|     |     | The flowgraph model for this program is identical to D |     |     |     |     |     |     |     |     |     |  in Figure 9.2. |     |     |     |     |
| --- | --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- |
3
|     |     | Strictly  |     | speaking,  |     | a  flowgraph  |     |     | is  “parameterized”  |     |     | when  |     | we  associ- |     |     |
| --- | --- | --------- | --- | ---------- | --- | ------------- | --- | --- | -------------------- | --- | --- | ----- | --- | ----------- | --- | --- |
ate with it the actual code that it represents. For example, the notation
* The sequence statement P  is a special case of a sequence of n statements P . Another special
|     |     |               |     |                                                                                  | 2   |     |     |     |     |     |     |     | n   |     |     |     |
| --- | --- | ------------- | --- | -------------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | instance of P |     |  is the case n = 1, which represents a program consisting of a single statement. |     |     |     |     |     |     |     |     |     |     |     |     |
n

|     | 386  |   ◾    Software Metrics |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ---- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
support these primes. Thus, in these languages, the set of structured pro-
grams includes the set of S-graphs where
S = {P
|     |          |                     |     |     |     | , D , D | , D |     | , D , D | , C  (for all n), L |     |     |     | }   |     |     |     |     |
| --- | -------- | ------------------- | --- | --- | --- | ------- | --- | --- | ------- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |          |                     |     |     | 1   | 0       | 1   | 2   | 3       | 4 n                 |     |     |     | 2   |     |     |     |     |
|     | 9.2.1.3  | Prime Decomposition |     |     |     |         |     |     |         |                     |     |     |     |     |     |     |     |     |
We  can  associate  with  any  flowgraph  a  decomposition  tree  to  describe
how  the  flowgraph  is  built  by  sequencing  and  nesting  primes  (Fenton
and Whitty 1986). Figure 9.8 illustrates how a decomposition tree can be
determined from a given flowgraph.
Figure 9.9 presents another example, where a flowgraph is shown with
its prime decomposition tree.
To  understand  this  prime  decomposition,  consider  the  program-
ming constructs that correspond to the named primes. By expanding
is the sequence
The flowgraph F
|     |     | here |     |     | of this |     |     |     |     |     |     |     | But F |     |     |     |     |     |
| --- | --- | ---- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
1
|     |     |     |     |     | flowgraph F |     |     |     |     |     |     |     | is the prime |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
1
D
1
with the prime
Prime decomposition
and this
D  nested
2
prime D
|     |     |     |              |     |     |     | 0         |     |     |        |     |     | onto it    |     |     |     |      |        |
| --- | --- | --- | ------------ | --- | --- | --- | --------- | --- | --- | ------ | --- | --- | ---------- | --- | --- | --- | ---- | ------ |
|     |     |     | A structured |     |     |     | flowgraph |     |     | caSneq |     | be  | decomposed |     |     |     | into | primes |
Thus, the
|     |     |     |     |                           |     |     | hierarchical |     |     |     | D   | D   |                       |     |     |     |     |     |
| --- | --- | --- | --- | ------------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- |
|     |     |     |     | Corresponds to a structu1 |     |     |              |     |     |     | red |     | 0program construction |     |     |     |     |     |
decomposition
|     |             |     |                                                 |        |     |      |                |               |     |         |     | i.e.,  F = (D |     |  (D | )) ; D |     |     |     |
| --- | ----------- | --- | ----------------------------------------------- | ------ | --- | ---- | -------------- | ------------- | --- | ------- | --- | ------------- | --- | --- | ------ | --- | --- | --- |
|     |             |     |                                                 |        |     |      |                |               |     |         |     |               |     | 1 2 | 0      |     |     |     |
|     |             |     |                                                 |        |     |      | into primes is |               |     |         | D   |               |     |     |        |     |     |     |
|     |             |     | The decomposition                               |        |     |      |                |               | is  | uni2que |     |               |     |     |        |     |     |     |
|     |             |     |                                                 | Can be |     | done |                | automatically |     |         |     |               |     |     |        |     |     |     |
|     | FIGURE 9.8  |     | Deriving the decomposition tree of a flowgraph. |        |     |      |                |               |     |         |     |               |     |     |        |     |     |     |
Measuring Internal Product Attributes    ◾    387
|     |     |     |     |        |     |                  | Measuring Internal Product Attributes  |     |     |     |              |     |     |     |   ◾    387   |     |     |     |
| --- | --- | --- | --- | ------ | --- | ---------------- | -------------------------------------- | --- | --- | --- | ------------ | --- | --- | --- | ------------ | --- | --- | --- |
|     |     |     |     | Allows |     | to check whether |                                        |     |     |     | a program is |     |     |     | S-structured |     |     |     |
if  a
if  a
|     |     |     | F   |     |     | a   |     |     | TREE(F) |     |     |     |     | a   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    then
|     |     |     |     |     |     |     |     |     |     then |     |     | D   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1
      begin
|     |     |     |     |     |     |     |     |     |       begin |     |     |     | b   |     | c   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | b   |     | c   |     |             |     |     |     |     |     |     |     |     |     |
         If b then do X;
|     |     |     |     |     |     |     |     |     |             | If b then do X;  |     |     |     |     |     |             |              |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---------------- | --- | --- | --- | --- | --- | ----------- | ------------ | --- |
|     |     |     |     |     |     |     |     |     |             | P                |     | X   |     |     | D   |             |              |     |
|     |     |     |     | X   |     |     |     |     |             |                  |     |     |     |     | 0   |          Y; |              |     |
|     |     |     |     |     |     |     |     |     |          Y; | 3                |     |     |     |     |     |             |              |     |
|     |     |     |     |     |     |     |     |     |             |                  |     |     |     |     | V   |             | while e do U |     |
|     |     |     |     |     |     | V   |     |     |             | while e do U     |     |     |     |     |     |             |              |     |
       end
       end
|     |     |     |     |     | Y   |     |     |     |            |     |     |     |     | Y   |     |          |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
|     |     |     |     |     |     |     |     |     | D          | P   | D   |     |     |     | D   |          |     |     |
|     |     |     |     |     |     |     |     |     |     else 0 | 1   | 2   |     |     |     | 3   |     else |     |     |
d
d
|     |     |     |     |     |     |     |     |     |          | if c |     |     |     |     |     |          | if c |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---- | --- | --- | --- | --- | --- | -------- | ---- | --- |
e
|     |     |     |     |     | e   |     |     |     |            | then  do  | U   |     |     |     |     |            | then  do  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | --- | --- | --- | --- | --- | ---------- | --------- | --- |
U
|     |     |     |     |     |     |     |     |     |                | repeat V until d F = D |     | ((D | ; P ; D | ), D (D | ))  |                | repeat V until d |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ---------------------- | --- | --- | ------- | ------- | --- | -------------- | ---------------- | --- |
|     |     |     |     |     |     |     |     |     |                |                        |     | 1 0 | 1       | 2 0     | 3   |                |                  |     |
FIGURE 9.10  The flowgraph of Figure 9.9 in terms of its program structure.
FIGURE 9.10  The flowgraph of Figure 9.9 in terms of its program structure.
36
|     | FIGURE 9.9  |     | A flowgraph and its decomposition tree. |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TREE(F) in Figure 9.9, we can recover the program text as shown in
TREE(F) in Figure 9.9, we can recover the program text as shown in
Figure 9.10.
Figure 9.10.
Not only can we always decompose a flowgraph into primes, but we can  Not only can we always decompose a flowgraph into primes, but we can
be assured that the decomposition is always unique: be assured that the decomposition is always unique:
Prime  decomposition  theorem:  Every  flowgraph  has  a  unique
Prime  decomposition  theorem:  Every  flowgraph  has  a  unique
decomposition into a hierarchy of primes.
decomposition into a hierarchy of primes.
The proof of the theorem (see (Fenton and Whitty 1986)) provides a
The proof of the theorem (see (Fenton and Whitty 1986)) provides a
constructive means of determining the unique decomposition tree. For
constructive means of determining the unique decomposition tree. For
large flowgraphs, it is impractical to perform this computation by hand,
large flowgraphs, it is impractical to perform this computation by hand,
but there are tools available commercially that do it automatically.
but there are tools available commercially that do it automatically.
The prime decomposition theorem provides us with a simple means  The prime decomposition theorem provides us with a simple means
of determining whether an arbitrary flowgraph is S-structured or not for  of determining whether an arbitrary flowgraph is S-structured or not for
some family of primes S. We just compute the decomposition tree and
some family of primes S. We just compute the decomposition tree and
look at the node labels; if every node is either a member of S or a P , then
look at the node labels; if every node is either a member of S or a P , then
n
n
the flowgraph is an S-graph.
the flowgraph is an S-graph.
|     | EXAMPLE 9.11 |     |     |     |     |     |     |     | EXAMPLE 9.11 |     |     |     |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
If S = {D , D }, then the flowgraph F in Figure 9.9 is not an S-graph, because  If S = {D , D }, then the flowgraph F in Figure 9.9 is not an S-graph, because
|     |     |     |     |     |     |     |     |     |     | 1 2 |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 1   | 2   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
one of the nodes in the decomposition tree is D . However, F is an SD-graph,
one of the nodes in the decomposition tree is D . However, F is an SD-graph,
|     |               |     |     |     |     |     |     |     |               | 3   |     |     |     |     |     |     | 3   |     |
| --- | ------------- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |               |     |     |     |     |     |     |     | where SD = {D |     | , D | , D | , D |     |     |     |     |     |
|     | where SD = {D |     | , D | , D | , D | }.  |     |     |               |     |     |     |     | }.  |     |     |     |     |
|     |               |     |     |     |     |     |     |     |               |     | 0   | 1   | 2   | 3   |     |     |     |     |
|     |               |     | 0   | 1   | 2   | 3   |     |     |               |     |     |     |     |     |     |     |     |     |
Every flowgraph must be S-structured for some family S (namely, where  Every flowgraph must be S-structured for some family S (namely, where
S is the set of distinct primes found in the decomposition tree); the ques- S is the set of distinct primes found in the decomposition tree); the ques-
tion is whether any members of S are considered to be “nonstructured.”  tion is whether any members of S are considered to be “nonstructured.”
The decomposition theorem shows that every program has a quantifiable  The decomposition theorem shows that every program has a quantifiable
degree of structuredness characterized by its decomposition tree. The only
degree of structuredness characterized by its decomposition tree. The only

|     |     | 386  |   ◾    Software Metrics |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ---- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
support these primes. Thus, in these languages, the set of structured pro-
grams includes the set of S-graphs where
|     |     |     |     | S = {P | , D | , D | , D | , D | , D | , C |  (for all n), L |     |     | }   |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
|     |     |     |     |        | 1   | 0   | 1   | 2   | 3   | 4   | n               |     |     | 2   |     |     |
9.2.1.3  Prime Decomposition
We  can  associate  with  any  flowgraph  a  decomposition  tree  to  describe
how  the  flowgraph  is  built  by  sequencing  and  nesting  primes  (Fenton
and Whitty 1986). Figure 9.8 illustrates how a decomposition tree can be
determined from a given flowgraph.
Figure 9.9 presents another example, where a flowgraph is shown with
its prime decomposition tree.
To  understand  this  prime  decomposition,  consider  the  program-
ming constructs that correspond to the named primes. By expanding
is the sequence
The flowgraph F
|     |     |     |     |     | of this |     |     |     |     |     |     |     | But F |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
here
1
|     |     |     |     |     | flowgraph F |     |     |     |     |     |     |     | is the prime |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- |
1
D
1
with the prime
and this
D  nested
2
prime D
onto it
0
|     |     |     | Hierarchical |     |     |     |     | measures |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Seq
Thus, the
|     |     |     |     |     |     |     | hierarchical |     |     |     | D   |     | D   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |              |     |     |     |     | 1   | 0   |     |     |     |
decomposition
Measures defined on the prime decomposition i.e.,  F = (D tree  (D )) ; D
|     |     |     |     |     |     |     |                |     |     |     |     |     |     | 1   | 2   | 0   |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | into primes is |     |     |     | D   |     |     |     |     |     |
2
|       |     | FIGURE 9.8  | Deriving the decomposition tree of a flowgraph. |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ----- | --- | ----------- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Depth |     |             | of nesting                                      |     |     |     |     |     |     |     |     |     |     |     |     |     |
d(P1) = 0
|     | d(F) = 1 for F ≠ P |     |     | in S |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ------------------ | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1
|     | d(F |     | ;F ) = maxF((d(F | ), d(F |     | ))  |     |     | TREE(F) |     |     |     |     |     |     |     |
| --- | --- | --- | ---------------- | ------ | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
D
|     |     | 1   | 2   | 1   |     | 2   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1
|     | d(F(F |     | , F )) = 1 + max((d(F |     |     | ), d(F |     | ))  |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --------------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |       |     | 1 2                   |     |     | 1      |     | 2   |     |     |     |     |     |     |     |     |
D
P
|     |     |     |     |     |     |     |     |     |     |     | 3   |     |     |     |     | 0   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     | D   | P   | D   |     |     |     |     | D   |
|     |     |     |     |     |     |     |     |     | 0   |     | 1   | 2   |     |     |     | 3   |
Example: d(F) = 3
|     |     |             |                                         |     |     |     |     |     |     |     | F = D | ((D | ; P | ; D ), D | (D  | ))  |
| --- | --- | ----------- | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | -------- | --- | --- |
|     |     |             |                                         |     |     |     |     |     |     |     |       | 1   | 0 1 | 2        | 0   | 3   |
|     |     | FIGURE 9.9  | A flowgraph and its decomposition tree. |     |     |     |     |     |     |     |       |     |     |          |     |     |
37

Measuring Internal Product Attributes    ◾    389
Next, assume that S is an arbitrary set of primes. We say a measure
m is a hierarchical measure if it can be defined on the set of S-graphs by
specifying:
: m(F) for each F ∈ S
M
1
M : The sequencing function(s)
2
 for each F ∈ S
M : The nesting functions h
|     | 3   |     |     |     |     |     | F   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
As we saw in Example 9.12, we may automatically compute a hierarchi-
cal measure for a program once we know M , M , M , and the decomposi-
1 2 3
tion tree.
The uniqueness of the prime decomposition implies that an S-graph can
be constructed in only one way. Thus, we can construct new hierarchical
measures simply by assigning a value m(F) to each prime and a value to
the sequence and nesting functions; in other words, we construct our own
conditions M , M , and M . However, rather than generating arbitrary and
|     |     |     | 1   |     | 2   | 3   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
artificial hierarchical measures in this way, we wish instead to show that
|     |     |     |     |     | Hierarchical |     |     | measures |     |
| --- | --- | --- | --- | --- | ------------ | --- | --- | -------- | --- |
many existing measures, plus many measures of specific intuitive struc-
tural attributes, are indeed hierarchical.
Define:
|     |     | M1: M(F) for each |     |     |     | F in S |     |     |     |
| --- | --- | ----------------- | --- | --- | --- | ------ | --- | --- | --- |
EXAMPLE 9.13
|     |     | M2: M(F |     |     | ;..;F | ) from | M(F ) |     |     |
| --- | --- | ------- | --- | --- | ----- | ------ | ----- | --- | --- |
|     |     |         |     |     | 1 n   |        | i     |     |     |
In ChapMte3r :8 M, w(Fe( Fdi,s.c.,uFss)e)d f rsoommeM o(fF th)e problems involved in defining the
|     |     |     |     |     | 1   | n   |     | i   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
lines of code measure unambiguously. Given the theory, which we have pre-
|     | Any | valid |     | M1, M2, M3 gives |     |     |     | a hierarchical | measure! |
| --- | --- | ----- | --- | ---------------- | --- | --- | --- | -------------- | -------- |
sented so far in this chapter, we define a formal size measure, v, which cap-
tures unambiguously the number of statements in a program when the latter
|     | Example: size v(F) (number |     |     |     |     |     |     | of nodes) |     |
| --- | -------------------------- | --- | --- | --- | --- | --- | --- | --------- | --- |
is modeled by a flowgraph.
M : v(P) = 1, and for each prime F ≠ P, v(F) = n + 1, where n is the num-
|     |     | 1   | 1   |     |     |     |     | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ber of procedure nodes in F
|     | M   | : v(F   | ; …; F |     | ) = Σv(F)                            |     |     |     |     |
| --- | --- | ------- | ------ | --- | ------------------------------------ | --- | --- | --- | --- |
|     |     | 2       | 1      |     | n                                    | i   |     |     |     |
|     | M   | : v(F(F | , …, F |     | )) = 1 + Σv(F) for each prime  F ≠ P |     |     |     |     |
|     |     | 3       | 1      |     | m                                    |     | i   |     | 1   |
Condition M  asserts that the size of a procedure node (which will gener-
1 38
ally correspond to a statement having no control flow) will be 1. The size of
a prime with n procedure nodes (which will generally be a control statement
involving n noncontrol statements) is n + 1. This mapping corresponds to our
intuitive notion of size, and satisfies the properties of the size attribute given
in  Section  8.1.  The  sequence  and  nesting  functions  given  in  M   and  M ,
2 3
respectively, are equally noncontroversial.

| 390  | Software Metrics |     |     |     |     |     |     |     |     |     |     |
| ---- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  ◾
To see how this measure works, we apply it to a flowgraph F in Figure 9.9:
|     | v(F) | = v(D      |     |  ((D | ;P;D           |     | ), D    |  (D | ))) |     |                 |
| --- | ---- | ---------- | --- | ---- | -------------- | --- | ------- | --- | --- | --- | --------------- |
|     |      |            |     | 1    | 0              | 1   | 2       | 0   | 3   |     |                 |
|     |      | = 1 + (v(D |     |      | ;P;D           |     | ) + v(D |     |  (D | ))) | (Nesting rule)  |
|     |      |            |     |      | 0              | 1   | 2       |     | 0   | 3   |                 |
|     |      | = 1 + (v(D |     |      | ) + v(P) + v(D |     |         |     | ))  |     | (Sequence rule  |
|     |      |            |     |      | 0              |     | 1       |     | 2   |     |                 |
and nesting rule)
|     |     |     |    + (1 + v(D |     |     | ))  |     |     |     |     |     |
| --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
3
= 1 + (2 + 1 + 2) + (1 + 2)
= 9
Once a hierarchical measure has been characterized in terms of the con-
ditions M , M , and M , then we have all the information we need to calcu-
|     | 1   |     | 2   |     | 3   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
late the measure for all S-graphs. We also have a constructive procedure for
calculating measures using this information together with the prime decom-
position tree. Some other simple but important hierarchical measures that
|     | More hierarchical |     |     |     |     |     |     |     |     |     | measures |
| --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- |
capture very specific properties are shown in Figure 9.11.
Number of Nodes Measure n
M : n(F) = number of nodes in F for each prime F
1
| M : n(F | ; …; F |     | ) = Σn(F) – k + 1                       |     |     | m   |     |     |     |     |     |
| ------- | ------ | --- | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2       | 1      | m   |                                         |     | i   |     |     |     |     |     |     |
|         | , …, F |     | )) = n(F) + Σn(F) – 2k for each prime F |     |     |     |     |     | p   |     |     |
M : n(F(F
| 3   | 1   |     | p   |     |     |     |     | i   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Number of Edges Measure e
M : e(F) = number of edges in F for each prime F
1
| M : e(F | ; …; F |     | ) = Σe(F)                              |     |     |     |     |     |     |     |     |
| ------- | ------ | --- | -------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2       | 1      | m   |                                        |     | i   |     |     |     |     |     |     |
|         | , …, F |     | )) = e(F) + Σe(F) – n for each prime F |     |     |     |     | m   |     |     |     |
M : e(F(F
| 3   | 1   |     | m   |     |     |     | i   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The “Largest Prime” Measure κ: (First Defined in Fenton (1985))
M : κ(F) = number of predicates in F for each prime F
1
| M : κ(F | ; …; F |     | ) = max(κ(F |     |     | ), …, κ(F |     |     | ))  |     |     |
| ------- | ------ | --- | ----------- | --- | --- | --------- | --- | --- | --- | --- | --- |
| 2       | 1      | n   |             |     |     | 1         |     | n   |     |     |     |
M : κ(F(F , …, F )) = max(κ(F), κ(F ), …, κ(F )) for each prime F
| 3   | 1   |     | n   |     |     |     |     | 1   |     | n   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Number of Occurrences of Named Primes Measure p
M : p(F) = 1 if F is named prime, else 0
1 39
|     | ; …; F |     | ) = Σp(F) |     |     |     |     |     |     |     |     |
| --- | ------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
M : p(F
| 2   | 1   | n   |     |     | i   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| M : p(F(F | , …, F |     | )) = p(F) + Σp(F) |     |     |     |     |     |     |     |     |
| --------- | ------ | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3         | 1      |     | m                 |     |     |     |     | i   |     |     |     |
D-Structured Measure d
(This nominal scale measure yields the value 1 if the flowgraph is D-structured and 0 if it
is not.)
| M : d(F) = 1 for F = P |        |                             |                    | , D | , D | , D       | , D |  and 0 otherwise |     |     |     |
| ---------------------- | ------ | --------------------------- | ------------------ | --- | --- | --------- | --- | ---------------- | --- | --- | --- |
| 1                      |        |                             |                    | 1   | 0   | 1         | 2   | 3                |     |     |     |
|                        | ; …; F |                             | ) = min(d(F        |     |     | ), …, d(F |     |                  |     |     |     |
| M : d(F                |        |                             |                    |     |     |           |     | ))               |     |     |     |
| 2                      | 1      | n                           |                    |     |     | 1         |     | n                |     |     |     |
| M : d(F(F              | , …, F |                             | )) = min(d(F), d(F |     |     |           |     | ), …, d(F        |     | ))  |     |
| 3                      | 1      |                             | n                  |     |     |           |     | 1                |     | n   |     |
| FIGURE 9.11            |        | Some hierarchical measures. |                    |     |     |           |     |                  |     |     |     |

Cyclomatic complexity
|     | Basis set:  | a maximal set of linearly |             |             |     |          |           |
| --- | ----------- | ------------------------- | ----------- | ----------- | --- | -------- | --------- |
|     | independent |                           | paths       |             |     |          |           |
| 1   | Any         | path                      | is a linear | combination |     | of paths | from the  |
basis sets
2
| 3   | e.g. | p = A B M |     |     | = (1 1 0 0 0 0 0 0 0) |     |     |
| --- | ---- | --------- | --- | --- | --------------------- | --- | --- |
1
|     |     | p = A B C E L B M |     |     | = (1 1 1 0 1 0 0 0 0) |     |     |
| --- | --- | ----------------- | --- | --- | --------------------- | --- | --- |
2
5
|     |     | p = A B C D F L B M  |     |     | = (1 1 0 1 0 1 0 0 0) |     |     |
| --- | --- | -------------------- | --- | --- | --------------------- | --- | --- |
4
3
p = A B C D G H L B M= (1 1 0 1 0 0 1 1 0)
4
| 7   |     | p = A B C D G I L B M  |     |     | = (1 1 0 1 0 0 1 0 1) |     |     |
| --- | --- | ---------------------- | --- | --- | --------------------- | --- | --- |
6
5
| 8 9 | Cyclomatic        |               | number:    |                |     |     |     |
| --- | ----------------- | ------------- | ---------- | -------------- | --- | --- | --- |
|     | the number        |               | of paths   | in a basis set |     |     |     |
|     | v(CFG) = #edges – |               |            | #nodes + 2     |     |     |     |
|     | = # decision      |               | points + 1 |                |     |     |     |
|     | e.g.              | v(CFG) = 14 – |            | 11 + 2 = 5     |     |     |     |
40

392 ◾ C Soyftwcalreo Mmetricas tic complexity measure
where d is the number of predicate nodes in F. Thus, ν can be defined as a
hiCeryarcchloicaml maetaiscurec ion mthep folleloxwiitnyg wisayh: ierarchical
M : ν(F) = 1 + d for each prime F, where d is the number of predicates
1
in F
M : ν(F , …, F ) = ∑n v(F ) − n + 1 for each n
2 1 n i=1 i
M : ν(F(F , …, F )) = v(F) + ∑n v(F ) − n for each prime F
3 1 n i=1 i
Thus, if ν is a measure of “complexity,” it follows that
1. The “complexity” of primes is dependent only on the number of
predicates contained in them.
2. The “complexity” of sequence is equal to the sum of the complexities
of the components minus the number of components plus one.
41
3. The “complexity” of nesting components on a prime F is equal to the
complexity of F plus the sum of the complexities of the components
minus the number of components.
From a measurement theory perspective, it is extremely doubtful that
any of these assumptions corresponds to intuitive relations about com-
plexity. Thus, ν cannot be used as a general complexity measure. However,
the cyclomatic number is a useful indicator of how difficult a program or
module will be to test and maintain. In this context, ν could be used for
quality assurance. In particular, McCabe has suggested that, on the basis
of empirical evidence, when ν is greater than 10 in any one module, the
module may be problematic.
EXAMPLE 9.14
Grady reported a study at Hewlett-Packard, where cyclomatic number was
computed for each module of 850,000 lines of FORTRAN code. The investi-
gators discovered a close relationship between a module’s cyclomatic num-
ber and the number of updates required. After examining the effects of cost
and schedule on modules with more than three updates, the study team
concluded that 15 should be the maximum cyclomatic number allowed in a
module (Grady 1994).

Design-level measures
| So far: intra-modular |     |     | measures |     |
| --------------------- | --- | --- | -------- | --- |
inside a procedure
| Now: inter-modular |                     |         | measures |          |
| ------------------ | ------------------- | ------- | -------- | -------- |
|                    | dependencies        | between | modules  |          |
| We                 | consider            | designs |          |          |
|                    | module structure is |         | the same | for code |
42

|     |     |     |     | Measuring Internal Product Attributes  |     |     |     |     |   ◾    403   |     |     |
| --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | ------------ | --- | --- |
Main
Scores
Scores
eof
|     |     | Read_Scores |     |     |     | Average |     |     |     |     |     |
| --- | --- | ----------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
Scores
Average
Average
|     |     |     |     | Calc_Av |     |     |     | Print_Av |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | --- | -------- | --- | --- | --- |
404   ◾   Software Metrics

of the whole system. This would correspond to a system with a centralized
|     | FIGURE 9.17  | Design charts. |     |     |     |     |     |     |     |     |     |
| --- | ------------ | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
control structure.
for example, in C, a procedure or function may be considered a module. In
For intramodular attributes, we consider models that capture the rel-
Java, a class or interface is considered a module. An individual Java or C++
evant details about information flow inside a module. Specifically, we look
at the dependencies among data. A data dependency graph (DDG) is a
method is considered a program unit, but not a module.
model of information flow supporting this kind of measurement (Bieman
To describe intermodular attributes, we build models to capture the nec-
and Debnath 1985). For instance, Figure 9.19 shows a simple program
essary information about the relationships between modules. Figure 9.17
fragments and their corresponding DDG models.
contains an example of a diagrammatic notation capturing the necessary
|     | details about designs (or code). |     |     |     | 9.3.2  | Global Modularity |     |     |     |     |     |
| --- | -------------------------------- | --- | --- | --- | ------ | ----------------- | --- | --- | --- | --- | --- |
This type of model describes the information flow between modules;
|     |     |     | Dependency |     | “Global modularity” is difficult to define because there are many different  |     | graph |     |     |     |     |
| --- | --- | --- | ---------- | --- | ---------------------------------------------------------------------------- | --- | ----- | --- | --- | --- | --- |
that is, it explains which variables are passed between modules. views of what modularity means. For example, consider average module
length as an intuitive measure of global modularity. As defined by any of
When measuring some attributes, we need not know the fine details
the measures in Chapter 8, module length is on a ratio scale, so we can
of a design, so our models suppress some of them. For example, instead
meaningfully consider average module length for a software system in
of examining variables, we may need to know only whether or not one
| We  | will | consider |     | dependency |     |     | graphs between |     |     |     |     |
| --- | ---- | -------- | --- | ---------- | --- | --- | -------------- | --- | --- | --- | --- |
terms of the mean length of all modules. Boehm cautions us to distinguish
module calls (or depends on) another module. In this case, we use a more
this type of measure from “complexity” or “structuredness”:
| modules |     |     |     |     |     |     |     |     | Measuring Internal Product Attributes   ◾   403   |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- |
abstract model of the design, a directed graph known as the module call-
“A metric was developed to calculate the average size of program mod-
graph; a call-graph is not a flowgraph, as it has no circled start or stop
ules as a measure of structuredness. However, suppose one has a software
• information flow
Main
node. An example is shown in Figure 9.18. product with n 100-statement control routines and a library of m 5-state-
Scores
|     |     |     |     |     | ment computational routines, which would be considered well structured  |     |     | Scores |     |     |     |
| --- | --- | --- | --- | --- | ----------------------------------------------------------------------- | --- | --- | ------ | --- | --- | --- |
Usually, we assume that the call-graph has a distinguished root node,
for any reasonable values of m and n. Then, if n = 2 and m = 98, the aver-
|     | corresponding to the highest-level module and representing an abstraction  |     |     |     |     |     |     | eof |     |     |     |
| --- | -------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  age module size is 6.9, while if m = 10 and n = 10, the average module size
|     |     |     |     |     |     |     |     | Read_Scores | Average |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | --- | --- |
is 52.5 statements” (Boehm et al. 1978).
|     |     |     |     | A   | Module A calls B, C |     |     |     | Scores |     |     |
| --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | ------ | --- | --- |
Average
Module B calls D We can describe global modularity in terms of several specific views of
• call graph Average
Module C calls D, E
modularity (Hausen 1989), such as the following:
C
|     |     |     |     |     |     |                         |     |                | Calc_Av | Print_Av |     |
| --- | --- | --- | --- | --- | --- | ----------------------- | --- | -------------- | ------- | -------- | --- |
|     |     |     | B   |     |     |                         |     |                |         |          |     |
|     |     |     |     |     |     | M  = modules/procedures |     |                |         |          |     |
|     |     |     |     |     |     | 1 FIGURE 9.17           |     | Design charts. |         |          |     |
E
D M  = modules/variables for example, in C, a procedure or function may be considered a module. In
2
Java, a class or interface is considered a module. An individual Java or C++
|                  |              |                    |     |     |     | method is considered a program unit, but not a module.                                | B                                                                        | X Y | C               |     |     |
| ---------------- | ------------ | ------------------ | --- | --- | --- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --- | --------------- | --- | --- |
|                  |              |                    |     |     |     | 0 Initialise                                                                          | 0                                                                        | 0 0 | 0 0 Initialise  | X   |     |
| Inside modules:  | FIGURE 9.18  | Module call-graph. |     |     |     |                                                                                       |                                                                          |     |                 | 0   | B   |
|                  |              |                    |     |     |     |                                                                                       | To describe intermodular attributes, we build models to capture the nec- |     |                 |     | 0   |
|                  |              |                    |     |     |     | 1 If X < Y                                                                            |                                                                          |     | 1 A = B         |     |     |
|                  |              |                    |     |     |     | 2 Then A = B essary information about the relationships between modules. Figure 9.17  |                                                                          |     | 2 While X > A D |     | A 1 |
0
data dependency graphs 3 Else A = C contains an example of a diagrammatic notation capturing the necessary  3 A = F(A,B)
A
2
|     |     |     |     |     |     | 4 D=A details about designs (or code). |     |     | 4 End | A   |     |
| --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | ----- | --- | --- |
|     |     |     |     |     |     |                                        |     | A   |       |     | 3   |
3
This type of model describes the information flow between modules;
that is, it explains which variables are passed between modules.
D
4
When measuring some attributes, we need not know the fine details
|     |     |     |     |     |              | of a design, so our models suppress some of them. For example, instead  |                                                    |     |     |     | 43  |
| --- | --- | --- | --- | --- | ------------ | ----------------------------------------------------------------------- | -------------------------------------------------- | --- | --- | --- | --- |
|     |     |     |     |     | FIGURE 9.19  |                                                                         | A data dependency graph model of information flow. |     |     |     |     |
of examining variables, we may need to know only whether or not one
module calls (or depends on) another module. In this case, we use a more
abstract model of the design, a directed graph known as the module call-
graph; a call-graph is not a flowgraph, as it has no circled start or stop
node. An example is shown in Figure 9.18.
Usually, we assume that the call-graph has a distinguished root node,
corresponding to the highest-level module and representing an abstraction

A Module A calls B, C
Module B calls D
Module C calls D, E
C
B
E
D
|     |     |     |     |     |     | FIGURE 9.18  |     | Module call-graph. |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------ | --- | ------------------ | --- | --- | --- |

Global modularity
Difficult to define, many views of modularity
Example: average module length
as a ratio: #modules / #procedures
or: #modules / #variables
44

|                              |     | Morphology |     |                     |              |          | measures |         |        |     |          |
| ---------------------------- | --- | ---------- | --- | ------------------- | ------------ | -------- | -------- | ------- | ------ | --- | -------- |
| Size: number                 |     |            |     | of nodes            | and/or edges |          |          |         |        |     |          |
| Depth: length                |     |            |     | of the longest      |              |          | path     |         |        |     |          |
| Width: maximum number        |     |            |     |                     |              | of nodes |          |         | at any |     | level    |
| 406    ◾    Software Metrics |     |            |     |                     |              |          |          |         |        |     |          |
| Edge-to-node                 |     |            |     | ratio: connectivity |              |          |          | density |        |     | measure  |
|                              |     |            |     |                     |              |          |          |         | Size   |     | 12 nodes |
a
15 edges
|     |     |     |     |     |     |     |     |     | Depth |     | 3   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
|     |     |     |     |     |     |     |     |     | Width |     | 6   |
d
c
|     |       |     |     | b   |     |     |     |     | Edge-to-node |     |      |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---- |
|     | Depth |     |     |     |     |     |     |     | Ratio        |     | 1.25 |
|     |       |     |     | f   |     | h   |     |     |              |     |      |
|     |       |     | e   |     | e   |     | i   |     | j            |     |      |
l
k
45
Width
| FIGURE 9.20          |     | A design and corresponding morphology measures. |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9.3.4  Tree Impurity |     |                                                 |     |     |     |     |     |     |     |     |     |
The graphs in Figure 9.21 represent different system structures that might
be found in a typical design. They exhibit properties that may help us to
judge good designs. We say that a graph is connected if, for each pair of
nodes  in  the  graph,  there  is  a  path  between  the  two.  All  of  the  graphs
in Figure 9.21 are connected. The complete graph, K , is a graph with n
n
nodes, where every node is connected to every other node, so there are
n(n − 1)/2 edges. Graphs G , G , and G  in Figure 9.21 are complete graphs
|     |     |     |     | 4 5 |     | 6   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
with three, four, and five nodes, respectively. The graph G  in Figure 9.21 is
1
called a tree, because it is a connected graph having no cycles (i.e., no path
that starts and ends at the same node). None of the other graphs is a tree,
because each contains at least one cycle.
|     |     | G   |     |     |     | G   |     |     |     | G   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 1   |     |     | 2   |     |     |     |     | 3   |

|     |     |     | G   |     |     | G   |     |     |     | G   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 4   |     |     | 5   |     |     |     | 6   |     |

FIGURE 9.21  Dependency graphs with varying degrees of tree impurity.

|                                    | Tree                                |                          | impurity  |       | measurement |               |                     |        |     |
| ---------------------------------- | ----------------------------------- | ------------------------ | --------- | ----- | ----------- | ------------- | ------------------- | ------ | --- |
| Idea: " The more a system deviates |                                     |                          |           |       |             |               | from                | being  | a   |
| pure tree                          |                                     | structure towards        |           |       | being       |               | a graph structure,  |        |     |
| the worse                          |                                     | the design is" (Ince     |           |       |             | & Hekmatpour) |                     |        |     |
| Measure                            |                                     | how far a graph deviates |           |       |             |               | from                | a tree |     |
| A measure                          |                                     |                          | M(G) such | that: |             |               |                     |        |     |
| •                                  | M(G) = 0 for a tree                 |                          |           | G     |             |               |                     |        |     |
| •                                  | M(G1) > M(G2) if G1 = G2 + one edge |                          |           |       |             |               |                     |        |     |
•
|         | M(G1) < M(G2) if G1 has more nodes |     |              |     |         |       | but the same |     |     |
| ------- | ---------------------------------- | --- | ------------ | --- | ------- | ----- | ------------ | --- | --- |
|         | number                             |     | of exceeding |     | edges   | as G2 |              |     |     |
| Several | possible definitions               |     |              |     | of M(G) |       |              |     |     |
46

Tree impurity: example
| For a graph G with |      | N nodes       | and E edges |     |
| ------------------ | ---- | ------------- | ----------- | --- |
| Spanning           | tree | has N-1 edges |             |     |
Complete graph has N (N-1) / 2 edges
| G has E-N+1 exceeding |     |     | edges |     |
| --------------------- | --- | --- | ----- | --- |
Complete graph has N (N-1) / 2 – (N-1)
= (N-1) (N-2) / 2 exceeding edges
| M(G) = #exceeding |     | edges | / max #exceeding | edges |
| ----------------- | --- | ----- | ---------------- | ----- |
= 2 (E-N+1) / (N-1) (N-2)
47

406   ◾   Software Metrics
Size 12 nodes
|     |     | a   |     | 15 edges |     |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- |
Depth 3
Width 6
d
|     |     | c   | Edge-to-node |     |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- | --- |
b
| Depth |     |     | Ratio | 1.25 |     |     |     |
| ----- | --- | --- | ----- | ---- | --- | --- | --- |
|       |     | f   | h     |      |     |     |     |
|       | e   |     | e i j |      |     |     |     |
l
k
Width
| FIGURE 9.20  | A design and corresponding morphology measures. |     |     |     |     |     |     |
| ------------ | ----------------------------------------------- | --- | --- | --- | --- | --- | --- |
9.3.4  Tree Impurity
The graphs in Figure 9.21 represent different system structures that might
be found in a typical design. They exhibit properties that may help us to
judge good designs. We say that a graph is connected if, for each pair of  Tree impurity: example
nodes in the graph, there is a path between the two. All of the graphs
| in Figure 9.21 are connected. The complete graph, K |     |     |     | , is a graph with n  |     |     |     |
| --------------------------------------------------- | --- | --- | --- | -------------------- | --- | --- | --- |
n
nodes, where every node is connected to every other node, so there are
| n(n − 1)/2 edges. Graphs G                                  |     | , G , and G |  in Figure 9.21 are complete graphs  |                     |     |     |     |
| ----------------------------------------------------------- | --- | ----------- | ------------------------------------ | ------------------- | --- | --- | --- |
|                                                             |     | 4 5         | 6                                    |                     |     |     |     |
| with three, four, and five nodes, respectively. The graph G |     |             |                                      |  in Figure 9.21 is  |     |     |     |
| M(G) = 2 (E-N+1) / (N1                                      |     |             |                                      | -1) (N-2)           |     |     |     |
called a tree, because it is a connected graph having no cycles (i.e., no path
that starts and ends at the same node). None of the other graphs is a tree,
because each contains at least one cycle.
|     | G   |     | G   | G   |       |              |      |
| --- | --- | --- | --- | --- | ----- | ------------ | ---- |
|     | 1   |     | 2   | 3   |       |              |      |
|     |     |     |     |     | E-N+1 | (N-1)(N-2)/2 | M(G) |
|     |     |     |     |     | G1 0  | 10           | 0    |
|     |     |     |     |     | G2 1  | 10           | 0.1  |

|     |     |     |     |     | G3 2 | 10  | 0.2 |
| --- | --- | --- | --- | --- | ---- | --- | --- |
|     | G   |     | G   | G   |      |     |     |
|     | 4   |     | 5   | 6   |      |     |     |
|     |     |     |     |     | G4 1 | 1   | 1   |
|     |     |     |     |     | G5 3 | 3   | 1   |
|     |     |     |     |     | G6 6 | 6   | 1   |

| FIGURE 9.21  | Dependency graphs with varying degrees of tree impurity. |     |     |     |     |     |     |
| ------------ | -------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
48

Summary
Principles of measurement
Goal, question, metric
Measurement of size attributes
Lines of code
Function points, COCOMO II
Measurement of structure attributes
Prime flowgraph decomposition,
hierarchical measures
Cyclomatic complexity
To follow: measurement of quality attributes
49

References
[FB] N.E. Fenton and J. Bieman. Software
Metrics: A Rigorous and Practical Approach. 3rd
edition, CRC Press, 2015.
Ch. 8, 9, 10
50

Software	  Quality Assurance
| 8b	  – | Software	  Measurement | II  |
| ------- | ----------------------- | --- |
Charles	  Pecheur
Apr 2017
1

PRODUCT METRICS: QUALITY
2

Internal	  and	  external	  attributes
| Previously:	           |               |                   |      | Now:	                  |                |            |
| ----------------------- | ------------- | ----------------- | ---- | ----------------------- | -------------- | ---------- |
| Internal                | product       | attributes        |      | External                | product        | attributes |
| Internal,	  structural |               |                   | view | External,	  functional |                | view       |
| Size,	  structure      |               |                   |      | Measure                 | quality        |            |
| Affect	  quality       |               | in	  some        | way  |                         |                |            |
| Easy                    | to	  measure |                   |      | Harder                  | to	  measure  |            |
| Available               | early         | (design,	  code) |      | Available               | late (product) |            |
3

Software quality measures
The transcendental view:
What is software quality?
Quality is an ideal that we
thrive to but cannot attain
Depends on who you ask
The user view:
Quality is fitness for purpose,
"Quality is in the eyes of the beholder"
reliability, absence of defects
The manufacturing view:
Quality is conformance to the
process
The product view:
Quality is showing good
inherent characteristics
Quality is a composite of many
The value-­‐based view:
characteristics Quality is how much the
customer is willing to pay for it
⇒
Quality models
4

Product Quality Models
Does a product have desirable attributes?
product = document, file, system, …
attributes = completeness, consistency, reliability, …
Product quality models
hierarchical nomenclature of
product quality caracteristics
Baselines and targets
5

444 ◾ Software Metrics
McCall's quality model (1977)
Use Factor Criteria
Operability
Training
Usability
Communicativeness
I/O volume
Integrity
I/O rate
Product
Efficiency Access control
operation
Access audit
Correctness Storage efficiency
Execution efficiency
Reliability Traceability
Completeness
Maintainability Accuracy
Error tolerance
Metrics
Product
Testability Consistency
revision
Simplicity
Flexibility Conciseness
Instrumentation
Reusability Expandability
Product Generality
Portability
transition
Self-descriptiveness
Modularity
Interoperability
Machine independence
S/w system indpendence
Comms commonality
Data commonality
FIGURE 10.2 McCall software quality model.
EXAMPLE 10.1
In McCall’s model, the factor reliability is composed of the criteria (or subfac-
tors) consistency, accuracy, error-tolerance, and simplicity.
Sometimes the quality criteria are internal attributes, such as structured-
ness and modularity, reflecting the developers’ belief that the internal attri-
butes have an affect on the external quality attributes. A further level of
decomposition is required, in which the quality criteria are associated with
a set of low-level, directly measurable attributes (both product and process)
called quality metrics. For instance, Figure 10.3 shows how maintainability
can be described by three subfactors and four metrics, forming a complete
decomposition. (This structure has been adapted from an IEEE standard for
software quality metrics methodology, which uses the term subfactor rather
than criteria (IEEE Standard 1061 2009).)
6

Measuring External Product Attributes ◾ 443
general interest, we show how the models and their derivatives may then
be tailored for individual purpose.
In Chapter 1, we introduced the notion of describing quality by enumer-
ating its component characteristics and their interrelationships. Figure 1.2
presented an example of such a quality model. Let us now take a closer
look at this type of model to see how it has been used by industry and what
we can learn from the results.
10.1.1 Early Models
Two early models described quality using a decomposition approach
(McCall et al. 1977; Boehm et al. 1978). Figure 10.1 presents the Boehm et al.
view of quality’s components, while Figure 10.2 illustrates the McCall et al.
view.
In models such as these, the model-builders focus on the final product
(usually the executable code), and identify key attributes of quality from
the user’s perspective. These key attributes, called quality factors, are nor-
mally high-level external attributes like reliability, usability, and main-
tainability. But they may also include several attributes that arguably are
internal, such as testability and efficiency. Each of the models assumes that
the quality factors are still at too high a level to be meaningful or to be
measurable directly. Hence, they are further decomposed into lower-level
Boehm's quality model (1978)
attributes called quality criteria or quality subfactors.
Primary uses Intermediate constructs Primitive constructs
Device independence
Completeness
Portability
Accuracy
Consistency
Reliability
As is utility
Device efficiency
Efficiency
Accessibility
General utility Metrics
Human engineering
Communicativeness
Testability
Maintainability Structuredness
Self-descriptiveness
Understandability
Conciseness
Modifiability
Legability
Augmentability
FIGURE 10.1 Boehm software quality model. 7

Elements of a quality model
Measuring External Product Attributes ◾ 445
Quality factor Quality subfactor Metric
Closure time
Fault counts Isolate/fix time
Fault rate
Correctability
Statement coverage
Degree of testing
Branch coverage
Test plan completeness
Maintainability Testability
Effort Resource prediction
Effort expenditure
Expandability
Change effort
Change counts Change size
Change rate
FIGURE 10.3 A decomposition of maintainability.
8
This presentation is helpful, as we may use it to monitor software qual-
ity in two different ways:
1. The fixed model approach: We assume that all important quality fac-
tors needed to monitor a project are a subset of those in a published
model. To control and measure each attribute, we accept the model’s
associated criteria and metrics and, most importantly, the proposed
relationships among factors, criteria, and metrics. Then, we use the
data collected to determine the quality of the product.
2. The “define your own quality model” approach: We accept the gen-
eral philosophy that quality is composed of many attributes, but we
do not adopt a given model’s characterization of quality. Instead, we
meet with prospective users to reach a consensus on which quality
attributes are important for a given product. Together, we decide on
a decomposition (possibly guided by an existing model) in which
we agree on specific measures for the lowest-level attributes (crite-
ria) and specific relationships between them. Then, we measure the
quality attributes objectively to see if they meet specified, quantified
targets.
The Boehm and McCall models are typical of fixed quality models.
Although it is beyond the scope of this book to provide a detailed and
exhaustive description of fixed model approaches, we present a small pic-
ture of how such a model can be used.
high-­‐level lower-­‐level
user's perspective quality criteria directly measurable

|                               | Using |           | a	  Quality |     |     | Model |
| ----------------------------- | ----- | --------- | ------------ | --- | --- | ----- |
| A	  checklist	  for	  each |       | criterion |              |     |     |       |
Example:	  Correctness /	  Completeness [Requirements,	  Design,
Implementation]:
• Unambiguous references (input,	  function,	  output)	  [R,D,I].
• All	  data	  references defined,	  computed,	  or	  obtained from external
• source	  [R,D,I].
•
| All	  defined |     | functions | used | [R,D,I].	   |     |     |
| -------------- | --- | --------- | ---- | ------------ | --- | --- |
•
| All	  referenced |     | functions |     | defined | [R,D,I].	   |     |
| ----------------- | --- | --------- | --- | ------- | ------------ | --- |
•
All	  conditions	  and	  processing defined for	  each decision point	  [R,D,I].
• All	  defined and	  referenced calling sequence parameters agree [D,I].
| • All	  problem   |     | reports	  resolved                                               |                | [R,D,I].	   |          |     |
| ------------------ | --- | ----------------------------------------------------------------- | -------------- | ------------ | -------- | --- |
| • Design	  agrees |     | with                                                              | requirements   |              | [D].	   |     |
| • Code	  agrees   |     | with                                                              | design	  [I]. |              |          |     |
| completeness       |     | =	  (#R	  /	  6	  +	  #D	  /	  8	  +	  #I	  /	  8)	   |                |              |          |     |
9

|                  |      | Define-­‐your-­‐own |              |     |               |        | model |
| ---------------- | ---- | ------------------- | ------------ | --- | ------------- | ------ | ----- |
| Boehm,	  McCall |      |                     | are	  fixed |     | models        |        |       |
| We               | can  | instead             | define       |     | our own       | models |       |
|                  | Keep | general             | philosophy   |     | of	  quality | models |       |
Factors,	  criteria,	  metrics
|                            | Select	  attributes |                            |            | suited              | for	  a	  particular |                            | product |
| -------------------------- | -------------------- | -------------------------- | ---------- | ------------------- | ---------------------- | -------------------------- | ------- |
|                            |                      | Discuss                    | with       | customers,	  users |                        |                            |         |
|                            |                      | Possibly                   | taken      | from                | some fixed             | model                      |         |
|                            | Refine               | to	  criteria,	  metrics |            |                     |                        |                            |         |
| Design	  by	  measurable |                      |                            |            |                     | objectives             |                            |         |
|                            | Measurable           |                            | attributes |                     | identified             | in	  the	  specification |         |
Apllicable to	  small,	  evolutionary development,	  agile	  processes
10

ISO	  Standard	  Quality Models
McCall's model	  	  →	  	  ISO	  9126-­‐1	  (2003)	  	  →	  	  ISO	  25010	  (2011)
| 8	  factors            | (supposed | to	  cover       | everything) |         |
| ----------------------- | --------- | ----------------- | ----------- | ------- |
| ISO	  25040	  defines |           | the	  evaluation |             | process |
11

|     |     | Measuring |     |     | quality |     |     |
| --- | --- | --------- | --- | --- | ------- | --- | --- |
Based	  on	  simple	  ratios
ET
| Example:	   |     | portability |     | =	  1	  – |     |     |     |
| ------------ | --- | ----------- | --- | ----------- | --- | --- | --- |
ER
|          | where   | ET	  =	  resources |                               |     | needed                    | to	  move	  to	  target |                |
| -------- | ------- | -------------------- | ----------------------------- | --- | ------------------------- | -------------------------- | -------------- |
|          |         | ER	  =	  resources |                               |     | needed                    | to	  create               | at	  resident |
| Factors  | depend  |                      | on	  subjective	  judgments |     |                           |                            |                |
| Requires | careful |                      | planning                      |     | and	  data	  collection |                            |                |
Uses	  resources
12

Measuring External Product Attributes    ◾    451
PHP 5.3 (538 KLOC), and PostreSQL 9.1 (1106 KLOC). Figure 10.5 shows
how the defect density can vary (Coverity 2011). Note that the defect d  ensities
reported by Coverity in these three open source systems are approximately
100 times lower than defect densities reported in commercial systems 25
years ago (Grady and Caswell 1987).
Defect density is certainly an acceptable measure to apply to your proj-
ects, and it provides useful information. However, the limitations of this
metric were made very clear in prior chapters. Before using it, either for
your own internal quality assurance purposes or to compare your perfor-
mance with others, you must remember the following:
| Defect-­‐based |     |     |     | quality | measures |     |
| -------------- | --- | --- | --- | ------- | -------- | --- |
  1. As discussed in Chapter 5, there is no general consensus on what
constitutes a defect. A defect can be either a fault discovered during
review and testing (which may potentially lead to an operational fail-
Narrow	  view:
ure), or a failure that has been observed during software operation.
| Quality | =	  lack | of	  defects |     |     |     |     |
| ------- | --------- | ------------- | --- | --- | --- | --- |
In published studies, defect counts have included
|                   |                                     |           | a.  Post-release failures                                       |     |     |     |
| ----------------- | ----------------------------------- | --------- | --------------------------------------------------------------- | --- | --- | --- |
| Defects           | =	  errors,	  faults,	  failures |           |                                                                 |     |     |     |
|                   |                                     |           | b.  Residual faults (i.e., all faults discovered after release) |     |     |     |
| Known             | defects                             | (from     | testing,	  inspection,	  …)                                   |     |     |     |
|                   |                                     |           | c.  All known faults                                            |     |     |     |
| Latent	  defects |                                     | (unknown) |                                                                 |     |     |     |
  d.  The set of faults discovered after some arbitrary fixed point in the
software life cycle (e.g., after unit testing)
#	  known	  defects
|     | Defect | density | =	   |     |     |     |
| --- | ------ | ------- | ----- | --- | --- | --- |
product	  size
Defect density (defects/KLOC)
0.7
| Example | (Coverity | 2011) |     |     |     |     |
| ------- | --------- | ----- | --- | --- | --- | --- |
0.6
0.5
0.4

0.3
0.2
0.0
0
13
|     |     |     |     | Linux 2.6 | PHP 5.3 | PostgreSQL 9.1 |
| --- | --- | --- | --- | --------- | ------- | -------------- |
FIGURE 10.5  Reported defect densities (Defects/KLOC) in three open source
systems (Coverity 2011).

|     |     | Defect |     | density |     | issues |     |
| --- | --- | ------ | --- | ------- | --- | ------ | --- |
•
| What | counts |     | as	  defects? |     |     |     |     |
| ---- | ------ | --- | -------------- | --- | --- | --- | --- |
faults,	  failures,	  post-­‐test,	  post-­‐release,	  …
•
| What | counts |     | as	  size? |     |     |     |     |
| ---- | ------ | --- | ----------- | --- | --- | --- | --- |
comments,	  data,	  binaries,	  tests,	  …
•
Do	  not	  confuse:
|       | defect | density  |     | =	  #	  defects | /	  size |     |     |
| ----- | ------ | -------- | --- | ----------------- | --------- | --- | --- |
| ≠	   | defect | rate	   |     | =	  #	  defects | /	  time |     |     |
• Depends on	  the	  quality of	  	  defect finding and
reporting
•
| #	  defects |     | does | not	  determine |     | operational |     | reliability |
| ------------ | --- | ---- | ---------------- | --- | ----------- | --- | ----------- |
depends on	  seriousness of	  defects,	  usage	  of	  system
| hard	  to	  predict |     |     | impact	  of	  faults |     |     |     |     |
| --------------------- | --- | --- | ---------------------- | --- | --- | --- | --- |
14

|     |     |     |     | Measuring External Product Attributes  |     |     |     |     |   ◾    453   |
| --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | ------------ |
Adams, who examined IBM operating system data, has highlighted the
dramatic difference in rate of failure occurrence.
EXAMPLE 10.5
Ed Adams at IBM examined data on nine software products, each with many
thousands of years of logged use worldwide (Adams 1984). He recorded the
information in Table 10.1, relating detected faults to their manifestation as
observed failures. For example, Table 10.1 shows that for product 4, 11.9% of
all known defects led to failures that occur on average every 160–499 years
of use.
Adams discovered that about a third of all detected faults lead to the
“smallest” types of failures, namely, those that occur on average every 5000
years (or more) of run-time. Conversely, a small number of faults (<2%) cause
the most common failures, namely those occurring at least once every 5
years of use. In other words, a very small proportion of the faults in a sys-
tem can lead to most of the observed failures in a given period of time;
conversely, most faults in a system are benign, in the sense that in the same
given period of time they will not lead to failures. In addition, less than 2%
of the failures were classified as “important failures.” Figure 10.6 summarizes
the relationship between faults, failures, and the distribution of the severity
of the failures.
It is quite Fposasibule tlot hasve paronducdts w	  iftha a ivelruy larrgee nsumber of faults
failing very rarely, if at all. Such products are certainly high quality, but
their quality is not reflected in a measure based on fault counts. It follows
| Study  | on	  9	  products |     |      | at	  IBM |     |     |     |     |     |
| ------ | ------------------- | --- | ---- | --------- | --- | --- | --- | --- | --- |
| Faults | →	  failure        |     | MTTF |           |     |     |     |     |     |
TABLE 10.1  Adams Data: Fitted Percentage Defects—Mean Time to Problem
Occurrence in Years
|     |         | 1.6   | 5     | 16    | 50    | 160   | 500   | 1600  | 5000  |
| --- | ------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
|     | Product | Years | Years | Years | Years | Years | Years | Years | Years |
|     | 1       | 0.7   | 1.2   | 2.1   | 5.0   | 10.3  | 17.8  | 28.8  | 34.2  |
|     | 2       | 0.7   | 1.5   | 3.2   | 4.5   | 9.7   | 18.2  | 28.0  | 34.3  |
|     | 3       | 0.4   | 1.4   | 2.8   | 6.5   | 8.7   | 18.0  | 28.5  | 33.7  |
|     | 4       | 0.1   | 0.3   | 2.0   | 4.4   | 11.9  | 18.7  | 28.5  | 34.2  |
|     | 5       | 0.7   | 1.4   | 2.9   | 4.4   | 9.4   | 18.4  | 28.5  | 34.2  |
|     | 6       | 0.3   | 0.8   | 2.1   | 5.0   | 11.5  | 20.1  | 28.2  | 32.0  |
|     | 7       | 0.6   | 1.4   | 2.7   | 4.5   | 9.9   | 18.5  | 28.5  | 34.0  |
|     | 8       | 1.1   | 1.4   | 2.7   | 6.5   | 11.1  | 18.4  | 27.1  | 31.9  |
|     | 9       | 0.0   | 0.5   | 1.9   | 5.6   | 12.8  | 20.4  | 27.6  | 31.2  |
33%
|     |        | 2%  |          |     |        | 65%      |     |          |          |
| --- | ------ | --- | -------- | --- | ------ | -------- | --- | -------- | -------- |
|     |        |     |          |     |        |          |     | smallest | failures |
|     | common |     | failures |     | benign | failures |     |          |          |
15

Other defect-­‐based measures
time to fix defects
Spoilage =
total development time
AT&T Bell Labs:
• Cumulative fault density—faults found internally
• Cumulative fault density—faults found by customers
• Total serious faults found
• Mean time to close serious faults
• Total field fixes
• High-­‐level design review errors per thousand NCLOC
• Low-­‐level design errors per thousand NCLOC
• Code inspection errors per inspected thousand NCLOC
• Development test and integration errors found per thousand NCLOC
• System test problems found per developed thousand NCLOC
• First application test site errors found per developed thousand NCLOC
• Customer found problems per developed thousand NCLOC
16

Usability
Usability is the	  degree to	  which a	  product or	  system
| can be | used | by	  specified |     | users | to	  achieve | specified |
| ------ | ---- | --------------- | --- | ----- | ------------- | --------- |
goals	  with effectiveness,	  efficiency and	  satisfaction
in	  a	  specified context of	  use.	  (ISO/IEC	  25010	  2011)
| User-­‐friendliness |     |     | (ease | to	  learn,	  use,	  remember) |     |     |
| ------------------- | --- | --- | ----- | --------------------------------- | --- | --- |
User	  satisfaction
| Not	  a	  directly |     | measurable |     | attribute |     |     |
| -------------------- | --- | ---------- | --- | --------- | --- | --- |
17

Usability measurement
Effectiveness
| %	  of	  correctly | completed        |               | tasks                   |             |     |
| -------------------- | ---------------- | ------------- | ----------------------- | ----------- | --- |
| User	  recall       | =	  remembering |               | information	  provided |             |     |
| task effectiveness   |                  | =	  quantity | × quality               | of	  tasks |     |
Efficiency
| Time	  to	  complete |     | a	  task,	  input	  rate          |           |      |      |
| ---------------------- | --- | ------------------------------------ | --------- | ---- | ---- |
| time	  efficiency     |     | =	  effectiveness                   | /	  task | time |      |
| productive	  period   |     | =	  productive	  time	  /	  task |           |      | time |
relative	  user	  efficiency =	  user	  efficiency /	  expert	  efficiency
Satisfaction
| Questionnaires,	  biological |     |     | measurements |     |     |
| ----------------------------- | --- | --- | ------------ | --- | --- |
18

Usability measurement
Not in ISO 25010:
Accessibility
disabilities (visual, hearing, physical)
Universality
cultural norms, naming conventions
Trustfulness
trust of users in the system (→ security)
19

| Usability |                            | measurement:	  internal |                  |     |
| --------- | -------------------------- | ------------------------ | ---------------- | --- |
| Internal  | elements                   | related                  | to	  usability: |     |
| •         | Good	  use	  of	  menus |                          | and	  graphics  |     |
•
|     | Informative	  error | messages |     |     |
| --- | -------------------- | -------- | --- | --- |
•
Help	  functions
•
Consistent	  interfaces
| •         | Well-­‐structured | manuals              |     |     |
| --------- | ----------------- | -------------------- | --- | --- |
| Can	  be | measured          | (size,	  structure) |     |     |
structure	  ⟷
| In	  particular,	  text      |                 |      | readability,	  comprehensibility |               |
| ------------------------------ | --------------- | ---- | --------------------------------- | ------------- |
| Poor	  measures               | of	  usability |      |                                   |               |
| as	  size,	  structure	  is |                 | poor | measure                           | of	  quality |
20

Maintainability
Maintainability is the	  degree of	  effectiveness and	  efficiency
with which a	  product or	  system	  can be modified by	  the
intended maintainers.	  (ISO/IEC	  25010	  2011)
Easy to	  understand,	  enhance,	  correct
| Maintenance	  can | be         |     |     |
| ------------------ | ---------- | --- | --- |
| • Corrective       | (fix bugs) |     |     |
•
| Adaptive     | (changes,	  upgrades) |          |        |
| ------------ | ---------------------- | -------- | ------ |
| • Preventive | (before                | failures | occur) |
| • Perfective | (enhance,	  extend)   |          |        |
Applies to	  code,	  documentation,	  specs,	  design,	  tests,	  …
| About	  making changes	  to	  the	  product |     |     |     |
| ----------------------------------------------- | --- | --- | --- |
21

|      | Maintainability      |     |     |        | measures |
| ---- | -------------------- | --- | --- | ------ | -------- |
| Mean | Time	  To	  Repair |     |     | (MTTR) |          |
average time	  to	  implement a	  change	  and	  restore
| the	  system	  to	  working |     |                         |                        | order.   |                    |
| ------------------------------ | --- | ----------------------- | ---------------------- | -------- | ------------------ |
| Measure                        |     | all	  times            |                        |          |                    |
| Problem                        |     | recognition	  time	   |                        |          |                    |
| Administrative	  delay        |     |                         |                        | time	   |                    |
| Maintenance	  tools           |     |                         | collection	  time	   |          |                    |
| Problem                        |     | analysis                | time	                 |          |                    |
| Change	  specification        |     |                         |                        | time	   |                    |
| Change	  time	  (including   |     |                         |                        | testing  | and	  review)	   |
22

|       | Maintainability |     |               | measures |     |
| ----- | --------------- | --- | ------------- | -------- | --- |
| Other | maintainability |     | measures:	   |          |     |
•
|     | change	  time	  /	  number |                  |     | of	  changes |     |
| --- | ----------------------------- | ---------------- | --- | ------------- | --- |
| •   | Number                        | of	  unresolved |     | problems      |     |
•
|     | Time	  spent        | on	  unresolved |           | problems      |     |
| --- | -------------------- | ---------------- | --------- | ------------- | --- |
| •   | %	  changes	  that |                  | introduce | new	  faults |     |
•
|     | Number | of	  modules	  modified |     |     | for	  a	  change	   |
| --- | ------ | ------------------------- | --- | --- | ---------------------- |
23

| Maintainability      |     |         | measures:	  internal  |     |
| -------------------- | --- | ------- | ---------------------- | --- |
| Internal	  elements |     | related | to	  maintainability: |     |
Structural	  complexity
Indication,	  not	  measure
| Use	  in	  correlation |                  | with                | external | measures  |
| ------------------------ | ---------------- | ------------------- | -------- | --------- |
|                          | e.g.	  identify | a	  module	  with | poor     | structure |
Readability
For	  texts
#	  words
| Fog | index	  F	  =	  0.4	  × |     |     | +	  %	  long	  words |
| --- | --------------------------- | --- | --- | ----------------------- |
#	  sentences
|     | (long	  word | =	  3	  or	  more	  syllables) |     |     |
| --- | ------------- | ---------------------------------- | --- | --- |
24

Security
Security	  is the	  degree to	  which a	  product or	  system
protects information	  and	  data	  so that persons or	  other
products or	  systems have	  the	  degree of	  data	  access
appropriate to	  their types	  and	  levels of	  authorization.
(ISO/IEC	  25010:2011)
| No	  "competent           |                                         | programmer"	  hypothesis: |       |                |                 |              |
| -------------------------- | --------------------------------------- | -------------------------- | ----- | -------------- | --------------- | ------------ |
| Assume	  that             |                                         | attackers                  | try   | to	  overcome |                 | security     |
| protections	  and	  hide |                                         |                            | their | activities     |                 |              |
| Risk                       | =	  Impact	  ×                        | Likelihood                 |       | × Threat       | × Vulnerability |              |
|                            | impact,	  likelihood,	  vulnerability |                            |       |                | depend          | on	  threat |
25

Security	  measures
| Common	  Vulnerability |         |               | Scoring | System	  (CVSS)	   |     |
| ----------------------- | ------- | ------------- | ------- | -------------------- | --- |
| metric                  | between | 0	  and	  1 |         |                      |     |
Six	  measures:
• Access	  vector (AV):	  how	  remote an	  attacker can be
• Access	  complexity (AC):	  how	  complex the	  attack needs to	  be
| • Authentication |     | (Au):	  how	  many |     | authentications | needed |
| ---------------- | --- | -------------------- | --- | --------------- | ------ |
•
| Confidentiality |     | impact	  (C):	  impact	  to	  system	   |     |     |     |
| --------------- | --- | -------------------------------------------- | --- | --- | --- |
• Integrity impact	  (I):	  impact	  to	  system	  integrity
•
Availability impact	  (A):	  reduced performance,	  shutdown
CVSS	  =	  f(AV,	  AC,	  Au,	  C,	  I,	  A)
26

Security	  measures
| Other measures:        |              |          |                   |              |
| ---------------------- | ------------ | -------- | ----------------- | ------------ |
| • Bayesian             |              | analysis | (probabilistic)   |              |
| based                  | on	  attack |          | probabilities     | and	  costs |
| • #	  vulnerabilities |              |          | /	  #	  defects |              |
| Internal               | measures:    |          |                   |              |
• Number of	  entry	  points,	  exit	  points,	  data
channels,	  persistent	  data	  items
27

Summary
| Quality | models:	  from |     | McCall | to	  ISO	  25010 |
| ------- | --------------- | --- | ------ | ------------------ |
8	  characteristics
4	  mostly addressed:	  reliability,	  maintainability,
usability,	  security
define-­‐your-­‐own
| Defect-­‐based |     | metrics |           |               |
| -------------- | --- | ------- | --------- | ------------- |
| not	  always  |     | precise | indicator | of	  quality |
Maintainability,	  Usability,	  security
28

References
[FB] N.E. Fenton and J. Bieman. Software
Metrics: A Rigorous and Practical Approach. 3rd
edition, CRC Press, 2015.
Ch. 8, 9, 10
29

Software Quality Assurance
9 – Software Reliability
Charles Pecheur
Apr 2017
1

|             | Why                  | Software	  Reliability |         |           |     |     |     |
| ----------- | -------------------- | ----------------------- | ------- | --------- | --- | --- | --- |
| Reliability | is                   | a	  key	  quality     |         | attribute |     |     |     |
| top-­‐level | in	  all	  quality |                         | models  |           |     |     |     |
| the	  most | extensively          |                         | studied |           |     |     |     |
Objectives
•
| Measure |     | failures |     |     |     |     |     |
| ------- | --- | -------- | --- | --- | --- | --- | --- |
•
| Predict       | future	  failures |                    |              | from | past        | failures |      |
| ------------- | ------------------ | ------------------ | ------------ | ---- | ----------- | -------- | ---- |
| • Reliability |                    | growth:	  predict |              |      | reliability |          | from |
| past          | faults             | found              | and	  fixed |      |             |          |      |
2

RELIABILITY THEORY
3

| Reliability       |              |     | theory          |
| ----------------- | ------------ | --- | --------------- |
| General	  theory | of	  system |     | and	  hardware |
reliability
Applicable	  to	  software	  reliability
| Basic	  question:	  when |                  | will | the	  system	  fail? |
| -------------------------- | ---------------- | ---- | ---------------------- |
| Software	  failures       | are	  different |      |                        |
from hardware	  failures
4

Failures:	  hardware	  	  vs	  software
| Hardware   |                        |     | Software	           |     |            |     |
| ---------- | ---------------------- | --- | -------------------- | --- | ---------- | --- |
| •          |                        |     | •                    |     |            |     |
| physical   | variability            |     | identical            |     | copies	   |     |
| • failures | due	  to	  wear,	   |     | • design	  bugs	   |     |            |     |
environnement
| •                 |         |        | •                           |             |         |          |
| ----------------- | ------- | ------ | --------------------------- | ----------- | ------- | -------- |
| reliability       | through |        | copies	  of	  program	   |             |         |          |
| redundancy        |         |        | share                       | the	  same |         | bugs	   |
| • reliability     | depends | on	   | • reliability               |             | depends | on	     |
| time              |         |        | execution                   |             | path    |          |
| • progressive	   |         |        | • abrupt	  degradation     |             |         |          |
degradation
5

Basic	  failure model
A	  component
| May	  fail | due	  to	  physical |                       |          | wear          |
| ----------- | --------------------- | --------------------- | -------- | ------------- |
| Probability |                       | that the	  component |          |               |
| will fail   | at	  time	  t       |                       |          |               |
| probability |                       | density               | function | (pdf)	  f(t) |
f(t)
t 6

Reliability Modelling
Failure probability density function
f(t) dt = Prob(failure between t and t+dt)
Failure probability distribution function
F(t) = ∫ f (t) dt = Prob(failure between 0 and t)
Reliability
R(t) = 1-­‐ F(t) = Prob(no failure before t)
f(t) F(t)
0
1
F(t) 1
0
R(t) t 7
t

Software Reliability    ◾    477
curve depends on the characteristics of the hose that affect the failure: the
materials, pressure, usage, etc. In this way, we build a model to describe
the likely failure.
The same approach applies in software. We build a basic model of com-
ponent reliability and create a probability density function (pdf) f of time t
(written as f(t)) that describes our uncertainty about when the component
will fail.
EXAMPLE 11.1
Suppose we know that a component has a maximum life span of 10 h. In
other words, we know it is certain to fail within 10 h of use. Suppose also
that the component is equally likely to fail during any two time periods of
equal length within 10 h. Thus, for example, it is just as likely to fail in the
first 2 min as in the last 2 min. Then we can illustrate this behavior with
the pdf f(t) shown in Figure 11.1. The function f(t) is defined to be 1/10 for
any t between 0 and 10, and 0 for any t  > 10. We say it is uniform in the
interval of time from t  =  0 to t  = 10. (Such an interval is written as [0,10].)
In general, for any x, we can define the uniform pdf over the interval [0,x]
to be 1/x for any t in the interval [0,x] and 0 elsewhere. Of special interest
(for technical reasons) is the pdf that is uniform on the interval [0,1].
| Example: |     | Uniform	  Density	  Function |     |     |     |     |     |
| -------- | --- | ------------------------------ | --- | --- | --- | --- | --- |
The uniform distribution in Example 11.1 has a number of limitations
for reliability modeling. For example, it applies to components only where
the failure time is bounded (and where the bound is known). In many situ-
Software	  will	  fail	  in	  the	  nateionxst, 	  n1o 0su	  chh obouunrds ,exists, and we need a pdf that reflects the fact that
there may be an arbitrarily long time to failure.
with	  uniform	  probability	  (unrealistic!)
| f(t)	  =	   | 1	  /	  10, | 0	  ≤	  t	  <	  10 |     |     |     |     |     |
| ------------- | ------------- | ---------------------- | --- | --- | --- | --- | --- |
|               | 0,            | 10	  ≤	  t           |     |     |     |     |     |
f(t)

| F(t)	  =	   | t	  /	  10, | 0	  ≤	  t	  <	  10 |     |     |     |     |     |
| ------------- | ------------- | ---------------------- | --- | --- | --- | --- | --- |
|               | 1,            | 10	  ≤	  t           |     |     |     |     |     |
1/10
| R(t)	  =	   | 1	  -­‐ t	  /	  10, | 0	  ≤	  t	  <	  10 |     |     |     |     |     |
| ------------- | ---------------------- | ---------------------- | --- | --- | --- | --- | --- |
480    ◾    Software Metrics
|          | 0,  | 10	  ≤	  t |              |               |     |     |     |
| -------- | --- | ------------ | ------------ | ------------- | --- | --- | --- |
|          |     |              |              |               | 0   | 10  | t   |
| F(t)     |     | R(t)         |              |               |     |     |     |
| F(t) = t |     |              | FIGURE 11.1  | Uniform pdf.  |     |     |     |
R(t) = 1–t
1
8
| 0   |     |     | 0   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | t   |     |     | 1 t |     |     |
1
FIGURE 11.3  Distribution function and Reliability function for uniform [0,1]
density function.
Thus,
|     |     | R(t) =  e−λt |     |     |     |     |     |
| --- | --- | ------------ | --- | --- | --- | --- | --- |
which is the familiar exponential reliability function. Both F(t) and R(t) are
shown in Figure 11.4.
Clearly, any one of the functions f(t), F(t), or R(t) may be defined in
terms of the others. If T is the random variable representing the yet-to-be-
observed time to failure, then any one of these functions gives a complete
description of our uncertainty about T. For example,
|     | P(T | > t) = R(t) | = 1 − F(t) |     |     |     |     |
| --- | --- | ----------- | ---------- | --- | --- | --- | --- |

where P stands for the probability function. The equation tells us that the
probability that the actual time to failure will be greater than a given time
t is equal to R(t) or 1 −  F(t). Thus, having any one of these functions allows
us to compute a range of specific reliability measures:
  R(t)
F(t)
| 1   |     | 1   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0   |     | t   | 0   |     | t   |     |     |
FIGURE 11.4  Distribution function and reliability function for exponential pdf.

|     | 478  | Software Metrics |     |     |     |     |     |
| --- | ---- | ---------------- | --- | --- | --- | --- | --- |
  ◾
EXAMPLE 11.2
Figure 11.2 illustrates an unbounded pdf that reflects the notion that the failure
time occurs purely randomly (in the sense that the future is statistically inde-
pendent of the past). The function is expressed as the exponential function
f(t) = λe−λt

In fact, the exponential function follows inevitably from the randomness
480    ◾    Software Metrics
assumption. As you study reliability, you will see that the exponential is cen-
tral to most reliability work.
| F(t) |     | R(t) |     |     |     |     |     |
| ---- | --- | ---- | --- | --- | --- | --- | --- |
F(t) = t
| 1   |     | R(t) = 1–t |     |     |     |     |     |
| --- | --- | ---------- | --- | --- | --- | --- | --- |
Having defined a pdf f(t), we can calculate the probability that the com-
ponent fails in a given time interval [t , t ]. Recall from calculus that this
1 2
probability is simply the area under the curve between the endpoints of
the interval. Formally, we compute the area by evaluating the integral:
0 0
|     | 1 t |     | 1   | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
t
∫ 1
|     | Probability of failure between time t |     |     |     |  and t | =   | f (t)dt. |
| --- | ------------------------------------- | --- | --- | --- | ------ | --- | -------- |
|     |                                       |     |     |     | 1      | 2   |          |
t
FIGURE 11.3  Distribution function and Reliability function for uniform [0,1]  2
density function.
EXAMPLE 11.3
Thus,
For the pdf in Example 11.1, the probability of failure from time 0 to time 2 h
|     | R(t) =  e−λt |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- |
is 1/5. For the pdf in Example 11.2, the probability of failure during the same
time interval is
which is the familiar exponential reliability function. Both F(t) and R(t) are
| shown in Figure 1C1.4.onstant	  Failure	  Rate |     |     | 2   |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
2
|     |     |     | ∫ λe−λt | ⎡−e−λt |        | e−2λ |     |
| --- | --- | --- | ------- | ------ | ------ | ---- | --- |
|     |     |     | dt      | =      | ⎤ = 1− |      |     |
|     |     |     |         | ⎣      | ⎦      |      |     |
|     |     |     |         |        | 0      |      |     |
0
Clearly, any one of the functions f(t), F(t), or R(t) may be defined in
When λ = 1, this value is equal to 0.63; when λ = 3, it is equal to 0.998.
terms of the others. If T is the random variable representing the yet-to-be-
Software	  will	  fail	  purely	  randomly
observed time to failure, then any one of these functions gives a complete
It follows from our definition that it does not make sense to consider the
description of our uncertainty about T. For example,
independently	  of	  the	  past,	  no	  memory
probability of failure at any specific instance of time t because this is always
| Constant	  probP(aT | b > it)li = tyR(	  tr)a | = t1e − 	  Fλ(t) |     |     |     |     |     |
| -------------------- | ------------------------ | ----------------- | --- | --- | --- | --- | --- |

  f(t)
f(t)	  =	   λ exp(-­‐λt)
where P stands for the probability function. The equation tells us that the
probability that the actual time to failure will be greater than a given time
λ
F(t)	  =	   1	  -­‐ exp(-­‐λt)
t is equal to R(t) or 1 −  F(t). Thus, having any one of these functions allows
us to compute a range of specific reliability measures:
R(t)	  =	   exp(-­‐λt)

| F(t) |     | R(t) | 0   |     |     |     | t   |
| ---- | --- | ---- | --- | --- | --- | --- | --- |
1
1
FIGURE 11.2  Pdf f(t) = λ eλt.
9
| 0   |     | 0   |     | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
t
FIGURE 11.4  Distribution function and reliability function for exponential pdf.

Example: Constant Failure Rate
Software will fail at constant probability rate
of once per hour
λ = 1 per hour = 1 / 3600
f(t) = (1 / 3600) exp(-­‐t / 3600)
F(t) = 1 -­‐ exp(-­‐t / 3600)
R(t) = exp(-­‐t / 3600)
R(1/λ) = exp(-­‐1) = 37%
10

Reliability, Availability, and Maintainability
Reliability:
operating without failure for a given time interval
time-­‐dependent R(t) = Prob(no failure before t)
Maintainability:
maintenance activity can be carried out within
stated time interval, procedures and resources
time-­‐dependent M(t) = Prob(restored before t)
Availability:
operating without failure at a given point in time
time-­‐independent A = Prob(not failed)
11

Measuring Reliability,
Availability, and Maintainability
Mean time to failure (MTTF):
average time before failure occurs
Measures reliability
Mean time to repair (MTTR):
average time to fix a fault
Measures maintainability
Availability: A = MTTF / (MTTF + MTTR)
12

MTTF and failure probability
MTTF = E(t) = ∫ t f(t) dt
Uniform distribution: f(t) = λ, 0 ≤ t ≤ 1/λ
)
"/$ ( "/$
MTTF = ∫ t λ dt = [λ ] = 1/2λ
%
%
*
Constant rate distribution: f(t) = λ exp(-­‐λt)
,
MTTF = ∫ t λ exp(−λt) dt = 1/λ
%
13

Hazard	  rate
Hazard	  rate	  (=	  failure rate)	  =	  probability density of	  failing
at	  time	  t,	  given that it has	  not	  failed before t.
f(t)
h(t)	  =
R(t)
Uniform	  distribution:
| h(t)	  =	  λ | /	  λ t | =	  1	  /	  t |     |     |
| -------------- | -------- | ---------------- | --- | --- |
Constant	  rate	  distribution:
| h(t)	  =	  λ	  exp(−λt)                 |         | /	  exp(−λt)	  =	  	  λ |                  |                     |
| ------------------------------------------ | ------- | --------------------------- | ---------------- | ------------------- |
| Rate	  of	  occurrence	  of	  failures |         |                             | (ROCOF)	  =	   |                     |
| probability                                | density | of	  any                   | failure          | (not	  necessarily |
the	  first)	  at	  time	  t
14

SOFTWARE RELIABILITY
15

Reliability growth
| Goal:	  Reliability |                   | growth |              |
| -------------------- | ----------------- | ------ | ------------ |
| failure              | rate	  decreases |        | over	  time |
| as	  faults         | are	  found      |        | and	  fixed |
may increase temporarily (ineffective	  fixes,	  new	  faults)
Assumptions:
• Software	  operating	  in	  a	  real (or	  simulated)
environment
• When failures occur,	  we attempt to	  find and	  fix the
| faults | that | caused | them |
| ------ | ---- | ------ | ---- |
16

Software Reliability   ◾   485
of novel faults. We can capture data to help us assess the short- and long-
term reliability by monitoring the time between failures. For example, we
can track execution time, noting how much time passes between succes-
sive failures.
Table 11.1 displays this type of data, expressing the successive execution
times, in seconds, between failures of a command-and-control system
during in-house testing using a simulation of the real operational envi-
ronment (Musa 1979). This data set is unusual, in that Musa took great
care in its collection. In particular, it was possible to obtain the actual
execution time, rather than merely calendar time (the relevance of which
was described in Chapter 5). As we read across the columns and down the
rows, our cursory glance detects improvement in reliability in the long
run: later periods of failure-free working tend to be significantly longer
than earlier ones. Figure 11.6 plots these failure times in sequence, and the
improvement trend is clearly visible.
However, the individual times vary greatly, and quite short times are
observed even near the end of the data set. Indeed, there are several zero
observations recorded, denoting that the system failed again immediately
after the previous problem was fixed. It is possible that the short inter-
failure times are due to inadequate fixes, so that the same problem per-
sists, or the fix attempt has introduced a new and severe problem. Musa
claimed that the zero times are merely short execution times rounded, as
are all these data, to the nearest second.
TABLE 11.1
Execution Times in Seconds between Successive Failures
Failure	  Data
|     | 3   | 30  | 113 | 81  | 115 |     | 9 2 | 91   | 112 | 15   |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- |
|     | 138 | 50  | 77  | 24  | 108 | 88  | 670 | 120  | 26  | 114  |
|     | 325 | 55  | 242 | 68  | 422 | 180 | 10  | 1146 | 600 | 15   |
|     | 36  | 4   | 0   | 8   | 227 | 65  | 176 | 58   | 457 | 300  |
|     | 97  | 263 | 452 | 255 | 197 | 193 | 6   | 79   | 816 | 1351 |
|     | 148 | 21  | 233 | 134 | 357 | 193 | 236 | 31   | 369 | 748  |
Time	  between	  successive
|     | 0   | 232 | 330 | 365 | 1222 | 543 | 10  | 16  | 529 | 379  |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- |
|     | 44  | 129 | 810 | 290 | 300  | 529 | 281 | 160 | 828 | 1011 |
failures
|     | 445 | 296  | 1755 | 1064 | 1783 | 860 | 983 | 707  | 33  | 868  |
| --- | --- | ---- | ---- | ---- | ---- | --- | --- | ---- | --- | ---- |
|     | 724 | 2323 | 2930 | 1461 | 843  | 12  | 261 | 1800 | 865 | 1435 |
From	  a	  command-­‐and-­‐control	   30 143 108 0 3110 1247 943 700 875 245
|     | 729 | 1897 | 447 | 386 | 446 | 122 | 990 | 948 | 1082 | 22  |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | ---- | --- |
system	  (Musa	  1979)
|     | 75   | 482 | 5509 | 100  | 10   | 1071 | 371 | 790 | 6150 | 3321 |
| --- | ---- | --- | ---- | ---- | ---- | ---- | --- | --- | ---- | ---- |
|     | 1045 | 648 | 5485 | 1160 | 1864 | 4116 |     |     |      |      |
Lots	  of	  variation
Note:  Read left to right in rows.
Growing
=>	  reliability	  is	  increasing
We	  cannot	  predict	  with
certainty	  when the	  next	  failure
will	  occur
17

Software Reliability   ◾   485
of novel faults. We can capture data to help us assess the short- and long-
term reliability by monitoring the time between failures. For example, we
can track execution time, noting how much time passes between succes-
sive failures.
Table 11.1 displays this type of data, expressing the successive execution
times, in seconds, between failures of a command-and-control system
during in-house testing using a simulation of the real operational envi-
ronment (Musa 1979). This data set is unusual, in that Musa took great
care in its collection. In particular, it was possible to obtain the actual
execution time, rather than merely calendar time (the relevance of which
was described in Chapter 5). As we read across the columns and down the
rows, our cursory glance detects improvement in reliability in the long
run: later periods of failure-free working tend to be significantly longer
than earlier ones. Figure 11.6 plots these failure times in sequence, and the
improvement trend is clearly visible.
However, the individual times vary greatly, and quite short times are
observed even near the end of the data set. Indeed, there are several zero
observations recorded, denoting that the system failed again immediately
after the previous problem was fixed. It is possible that the short inter-
failure times are due to inadequate fixes, so that the same problem per-
sists, or the fix attempt has introduced a new and severe problem. Musa
claimed that the zero times are merely short execution times rounded, as
are all these data, to the nearest second.
TABLE 11.1
Execution Times in Seconds between Successive Failures
Questions
|     |     | 3   | 30  | 113 | 81  | 115 |     | 9 2 | 91   | 112 | 15   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- |
|     |     | 138 | 50  | 77  | 24  | 108 | 88  | 670 | 120  | 26  | 114  |
|     |     | 325 | 55  | 242 | 68  | 422 | 180 | 10  | 1146 | 600 | 15   |
|     |     | 36  | 4   | 0   | 8   | 227 | 65  | 176 | 58   | 457 | 300  |
|     |     | 97  | 263 | 452 | 255 | 197 | 193 | 6   | 79   | 816 | 1351 |
|     |     | 148 | 21  | 233 | 134 | 357 | 193 | 236 | 31   | 369 | 748  |
When	  is	  the	  next	  failure?
|     |     | 0   | 232  | 330  | 365  | 1222 | 543  | 10  | 16   | 529 | 379  |
| --- | --- | --- | ---- | ---- | ---- | ---- | ---- | --- | ---- | --- | ---- |
|     |     | 44  | 129  | 810  | 290  | 300  | 529  | 281 | 160  | 828 | 1011 |
|     |     | 445 | 296  | 1755 | 1064 | 1783 | 860  | 983 | 707  | 33  | 868  |
|     |     | 724 | 2323 | 2930 | 1461 | 843  | 12   | 261 | 1800 | 865 | 1435 |
|     |     | 30  | 143  | 108  | 0    | 3110 | 1247 | 943 | 700  | 875 | 245  |
How	  reliable	  is	  it	  now?
|                                 |     | 729  | 1897 | 447  | 386  | 446  | 122  | 990 | 948 | 1082 | 22   |
| ------------------------------- | --- | ---- | ---- | ---- | ---- | ---- | ---- | --- | --- | ---- | ---- |
|                                 |     | 75   | 482  | 5509 | 100  | 10   | 1071 | 371 | 790 | 6150 | 3321 |
| Is	  it	  reliable	  enough? |     | 1045 | 648  | 5485 | 1160 | 1864 | 4116 |     |     |      |      |
Note:  Read left to right in rows.
How	  reliable	  will	  it	  be	  after
some	  additional	  effort?
How	  much	  effort	  until	  it	  is
reliable	  enough?
18

482 ◾ Software Metrics
f (t)
h(t) =
R(t)
h(t)δt is the probability that the component will fail during the interval [t,
t + δt], given that it had not failed before t.
EXAMPLE 11.8
The hazard rate for the important exponential pdf of Example 11.2 is λ.
So far, we have been concerned only with the uncertainty surrounding
the time at which the system fails for the first time. But, in many cases,
systems fail repeatedly (not always from the same cause), and we want to
understand the behavior of all these failures collectively. Thus, suppose
that a system fails at time t . We attempt to fix it (e.g., by replacing a par-
1
ticular component that has failed), and the system runs satisfactorily until
it fails at time t . We fix this new problem, and again, the system runs until
2
the next failure. After a series of i − 1 failures, we want to be able to predict
the time of the ith failure. This situation is represented in Figure 11.5.
Predicting failures
For each i, we have a new random variable t representing the time of
i
the ith failure. Each t has its own pdf f (and so, of course, also its own F
i i i
and R ). In classical hardware reliability, where we are simply replacing
i
Given a series of failure times t , t , …, t
failed components with identical working compo1nen2ts, we mii-­‐g1ht expect
the serifeas uofl tp dfifxs etod b ae fidteenrt iecaalc. hH ofwaielvuerr,e sometimes, we can replace each
failed component with one of superior quality. For example, we may be
Goal: predict future failure times T , T , …
able to make a design change to minimize the likelihood of recurrence of
i i+1
the fault that caused the previous one to fail. Here, we expect the pdf of
random variables f (and R and F )
i i i
t to be different from that of the pdf of t . In particular, we would expect
i+1 i
Past Now Future
Time
t t ... t t t ...
1 2 i–2 i–1 i
Time of last
Time of next (ith) failure
(i – 1th) failure
—to be predicted
19
FIGURE 11.5 Reliability problem for the scenario of attempting to fix failures
after each occurrence.

482 ◾ Software Metrics
f (t)
h(t) =
R(t)
h(t)δt is the probability that the component will fail during the interval [t,
t + δt], given that it had not failed before t.
EXAMPLE 11.8
The hazard rate for the important exponential pdf of Example 11.2 is λ.
So far, we have been concerned only with the uncertainty surrounding
the time at which the system fails for the first time. But, in many cases,
systems fail repeatedly (not always from the same cause), and we want to
understand the behavior of all these failures collectively. Thus, suppose
that a system fails at time t . We attempt to fix it (e.g., by replacing a par-
1
ticular component that has failed), and the system runs satisfactorily until
it fails at time t . We fix this new problem, and again, the system runs until
2
the next failure. After a series of i − 1 failures, we want to be able to predict
Predicting failures:
the time of the ith failure. This situation is represented in Figure 11.5.
For each i, we have a new random variable t representing the time of
hardware vs sofitware
the ith failure. Each t has its own pdf f (and so, of course, also its own F
i i i
and R ). In classical hardware reliability, where we are simply replacing
In hardware: replace failed components with
i
failed components with identical working components, we might expect
identical components
the series of pdfs to be identical. However, sometimes, we can replace each
⇒
f (t) ≈ f (t)
i i-­‐1
failed component with one of superior quality. For example, we may be
In software: fix faults
able to make a design change to minimize the likelihood of recurrence of
⇒
f (t) < f (t)
the fault that caused the previous one to fail. Here, we expect the pdf of
i i-­‐1
t to be different from that of the pdf of t . In particular, we would expect
Reliability growth
i+1 i
Past Now Future
Time
t t ... t t t ...
1 2 i–2 i–1 i
Time of last
Time of next (ith) failure
(i – 1th) failure
—to be predicted
20
FIGURE 11.5 Reliability problem for the scenario of attempting to fix failures
after each occurrence.

Elements of a Prediction System
Goal: predict the probability distributions F , F , …
i i+1
Prediction system has three elements:
• Prediction model: probability specification of
the stochastic process (distributions F (T ))
i i
• Inference procedure: infer unknown parameters
of the model from t , t , …, t
1 2 n-­‐1
• Prediction procedure: combine the model and
inference procedure to make predictions about
future failure behavior
21

Prediction system:	  example
• Model:	  constant	  failure rate
| F (t )	  =	  1	  -­‐ |     | exp(-­‐λ |     | t ) |
| ----------------------- | --- | -------- | --- | --- |
| i i                     |     |          |     | i i |
• Inference	  procedure:	  1/λ =	  average	  of	  two
i
previous	  times	  between	  failures
| λ =	  2	  /	  (t |     | +	  t |       | )   |
| ------------------- | --- | ------ | ----- | --- |
| i                   |     | i-­‐1  | i-­‐2 |     |
•
Prediction	  procedure:	  predict	  mean	  time	  to
next	  failure
| T =	  1/λ |     | =	  (t | +	  t | )	  /	  2 |
| ---------- | --- | ------- | ------ | ----------- |
| i          | i   | i-­‐1   |        | i-­‐2       |
22

Software Reliability ◾ 489
and solve for λ
i
2
λ =
i t + t
i−2 i−1
3. Prediction procedure. We calculate the mean time to ith failure by
substituting our predicted value of λ in the model. The mean time to
i
failure is 1/λ; so we have the average of the two previously observed
i
failure times. Alternatively, we can predict the median time to ith fail-
ure, which we know from Example 11.7 is equal to 1/λ log 2.
i
We can apply this prediction system to the data in Table 11.1. When
i = 3, we have observed t = 1 and t = 30. So, we estimate the mean of
1 2
the time to failure T to be 31/2 = 15.5. We continue this procedure for
3
each successive observation, t, so that we have:
i
a. For i = 4, we find that t = 30 and t = 113; so, we estimate T to be
2 3 4
71.5
b. For i = 5, we have t = 113 and t = 81; so, we estimate T to be 97
3 4 5
c. and so on
The results of this prediction procedure are depicted in Figure 11.7. Many
Prediction system: example
other, more sophisticated procedures could be used for the prediction. For
example, perhaps, our predictions would be more accurate if, instead of
using just the two previously observed values of t, we use the average of the
Predicting next failure times from pai st history
10 previously observed t. A plot for this variation, and for using the previous
i
a20v Nob=se ravveed rta, gise a losof slhaoswt nN i nt iFmiguerse t1o1. 7f.ailure
i
3000
Predicted mean time to failure (s)
2000
av10
av20
1000
av2
0 10 20 30 40 50 60 70 80 90 100 120 130 140 23
FIGURE 11.7 Plots from various crude predictions using data from Table 11.1.
The x-axis shows the failure number, and the y-axis is the predicted mean time to
failure (in seconds) after a given failure occurs.

490 ◾ Software Metrics
For predicting the median time to the next failure, our procedures are
similar. For this distribution, the median is 1/λ log 2 and the mean is 1/λ; so,
i i
the procedure is the same, except that all the results above are multiplied by
log 2 (i.e., by a factor of about 0.7).
Many prediction systems have been proposed, some of which use mod-
els and procedures far more sophisticated than Example 11.9. We as users
must decide which ones are best for our needs. In the next section, we
review several of the most popular models, each of which is parametric
(in the sense that it is a function of a set of input parameters). Then, we
can turn to questions of accuracy, as accuracy is critical to the success of
reliability prediction.
11.3 PARAMETRIC RELIABILITY GROWTH MODELS
Suppose we are modeling the reliability of our program according to the
Passaumrpationms of tehe tprreviiocus srecetionlsi, anambelyi lthiatt tyhe pgrogrraom iws opetraht-
ing in a real or simulated user environment, and that we keep trying to fix
faults after failures occur. We make two further assumptions about our
program:
Assumptions:
1. Executing the program involves selecting inputs from some space I
• Software operating in a real (or simulated) environment
(the totality of all possible inputs).
• When failures occur, we attempt to find and fix the faults
th2a. tThcea uprsoegrdamth teramnsforms the inputs into outputs (comprising a
space O).
And:
• ExThecisu trtainosnfor=m fatrioonm is isnchpemutatsicianlly s sphoawcne inI tFoig uoreu 1t1p.8u, wtsheirne Ps pisa ce O
a program transforming the inputs of I into outputs in O. For a typical
• Outputs are acceptable (pass) or unacceptable (fail)
program, the input space is extremely large; in most cases, a complete
• I = inputs leading to fail
description of the input space is not available. Also, different users may
F
I O
P
I
F Unacceptable
Acceptable
24
FIGURE 11.8 Basic model of program execution.

Uncertainty
We don't know where the faults are
Even if we did,
we don't know when or how they will cause a failure
Type-­‐1 uncertainty: how the system will be used
Type-­‐2 uncertainty: effect of fault removal
Reliability model must address both types
Type-­‐1 easier, type-­‐2 harder
25

492 ◾ Software Metrics
the mathematics can be daunting; complete understanding of the details
is not necessary for comparing and contrasting the models. However, the
details are useful for implementing and tailoring the models.
11.3.1 The Jelinski–Moranda Model
The Jelinski–Moranda model (denoted JM in subsequent figures) is the
earliest and probably the best-known reliability model (Jelinski and
Moranda 1972). It assumes that, for each i,
F(t ) = 1 − e−λ i t i
i i
with
λ = (N − i + 1) ϕ
i
Here, N is the initial number of faults, and ϕ is the contribution of each
fault to the overall failure rate. Thus, the underlying model is the expo-
nential model, so that the type-1 uncertainty is random and exponential.
There is no type-2 uncertainty in this model; it assumes that fault detec-
tion and correction begin when a program contains N faults, and that
fixes are perfect (in that they correct the fault causing the failure, and they
introduce no new faults). The model also assumes that all faults have the
Jelinski-­‐Moranda model
same rate. Since we know from Example 11.8 that the hazard rate for the
exponential distribution is λ, it follows that the graph of the JM hazard
rate looks like the step function in Figure 11.9. In other words, between the
(i − 1)th and ith failure, the hazard rate is (N − i + 1) ϕ.
Model: constant rate φ identical for all faults
F (t ) = 1 -­‐ exp(-­‐λ t ) Nϕ
i i i i
Step sizes equal
(N – 1)ϕ
λ = (N – i + 1) φ
i
(N – 2)ϕ
N = initial number of faults
(N – 3)ϕ
φ = failure rate for each fault
t t t t
1 2 3 4
Type-­‐1 uncertainty = random, exponential rate
FIGURE 11.9 JM model hazard rate (y-axis) plotted against time (x-axis).
No type-­‐2 uncertainty = corrections are perfect
Fixing any fault contributes equally to improving the
reliability
26

Jelinski-­‐Moranda model
Inference	  procedure:	  maximum	  likelihood
estimation	  (not	  detailed)
| Gives | predictions | for	  N | and	  φ |
| ----- | ----------- | -------- | -------- |
i i
Prediction	  procedure:	  predict	  mean	  time	  to
next	  failure
| T =	  1/λ | =	  1	  /	  (N | – i +	  1)	  φ |     |
| ---------- | ----------------- | ---------------- | --- |
| i          | i                 | i                | i   |
27

Jelinski-­‐Moranda model:	  example
494    ◾    Software Metrics
| TABLE 11.2  | Successive Failure Times for JM when  |     |     |
| ----------- | ------------------------------------- | --- | --- |
N = 15 and ϕ = 0.003
| i   | Mean Time      | Simulated Time  |     |
| --- | -------------- | --------------- | --- |
|     | to ith Failure | to ith Failure  |     |
| 1   | 22             |                 | 11  |
| 2   | 24             |                 | 41  |
| 3   | 26             |                 | 13  |
| 4   | 28             |                 | 4   |
| 5   | 30             |                 | 30  |
| 6   | 33             |                 | 77  |
| 7   | 37             |                 | 11  |
| 8   | 42             |                 | 64  |
| 9   | 48             |                 | 54  |
| 10  | 56             |                 | 34  |
| 11  | 67             |                 | 183 |
| 12  | 83             |                 | 83  |
| 13  | 111            |                 | 17  |
| 14  | 167            |                 | 190 |
| 15  | 333            |                 | 436 |
28
exponential distribution produces high variability, but generally, there is reli-
ability growth. Notice that as i approaches 15, the failure times become large.
Since the model assumes there are no faults remaining after i = 15, the mean
time to the 16th failure is said to be infinite.
There are three related criticisms of this model.
  1. The sequence of rates is considered by the model to be purely deter-
ministic. This assumption may not be realistic.
  2. The model assumes that all faults equally contribute to the hazard
rate.  The  Adams  example  in  Chapter  10  provides  empirical  evi-
dence that faults vary dramatically in their contribution to program
  unreliability.
  3. We show that the reliability predictions obtained from the model are
poor; they are usually too optimistic.
11.3.2  Other Models Based on JM
Several  models  are  variations  of  JM.  Shooman’s  model  is  identical
(Shooman 1983). The Musa model (one of the most widely used) has JM as
a foundation but builds some novel features on top (Musa 1975). It was the

| Jelinski-­‐Moranda |              |         | model:	  criticisms |     |                    |     |     |
| ------------------ | ------------ | ------- | -------------------- | --- | ------------------ | --- | --- |
| Unrealistic        | assumptions: |         |                      |     |                    |     |     |
| • The	  sequence  |              | of	  λ | is purely            |     | deterministic.	   |     |     |
i
•
| All	  faults | equally | contribute |     |     | to	  the	  hazard |     |     |
| ------------- | ------- | ---------- | --- | --- | ------------------- | --- | --- |
rate.
| The	  reliability | predictions |     |     | obtained |     | from | the	   |
| ------------------ | ----------- | --- | --- | -------- | --- | ---- | ------- |
model	  are	  poor;	  they are	  usually too optimistic.
29

Other models
Musa model
Jelinski-­‐Moranda + features (exec time + calendar time)
Littlewood model
Treats each corrected fault's contribution to reliability as
independent variable (γ-­‐distribution)
Two sources of uncertainty in the distribution
Littlewood-­‐Verrall model
Variant of Littlewood
Nonhomogeneous Poisson mdels (NHPP)
Goel-­‐Omukoto, Littlewood (LNHPP), Duane
30

Prediction models: comparison
Software Reliability ◾ 493
30 40 50 60 70 80 90 100 120 130 140
i
The inference procedure for JM is called maximum likelihood estimation;
its details need not concern us here, but a simple overview is provided in
Fenton and Neil (2012) while a description in the specific context of reli-
ability may be found in textbooks such as Rausand and Hoyland (2004),
Modarres et al. (2010), and Birolini (2007). In fact, maximum likelihood is
the inference procedure for all the models we present. For a given set of fail-
ure data, this procedure produces estimates of N and ϕ . Then, t is predicted
i i i
by substituting these estimates in the model. (We shall see the JM median
time to failure predictions in Figure 11.10, based on the data of Table 11.1.)
EXAMPLE 11.10
We can examine the reliability behavior described by the JM model to deter-
mine whether it is a realistic portrayal. Consider the successive inter-failure
times where N = 15 and ϕ = 0.003. Table 11.2 shows both the mean time
to the ith failure and also a simulated set of failure times (produced using
random numbers in the model). In the simulated data, the nature of the
naideM
3000
JM
GO
2000
LM
LNHPP
DU
1000
LV
(KL, MO
almost
identical)
FIGURE 11.10 Data analyzed using several reliability growth models. The cur-
rent median time to the next failure is plotted on the y-axis against failure num-
ber on the x-axis. We use the model abbreviations introduced in the previous
sections. Two additional models are considered here: KL (Keiller–Littlewood)
and MO (Musa–Okumoto).
31

|                                           |              |                                            | Statistical |                   |                 | Testing      |
| ----------------------------------------- | ------------ | ------------------------------------------ | ----------- | ----------------- | --------------- | ------------ |
| Reliability                               | predictions  |                                            |             | based             | on	            |              |
| failures                                  | occuring     |                                            | during      | testing           |                 |              |
| May	  not	  correspond	  to	  typical |              |                                            |             |                   | system	  usage |              |
| Different                                 |              | users,	  tasks,	  experience             |             |                   | levels,	  …    |              |
| Statistical                               | testing:	   |                                            |             |                   |                 |              |
| select	  tests	  according              |              |                                            |             | to	  operational |                 | profile      |
| probability                               |              | distribution	  on	  inputs	  reflecting |             |                   |                 | usage        |
| Operational                               |              | profiles	  are	  difficult               |             |                   |                 | to	  define |
| Statistical                               |              | usage	  can                               |             | be misleading     |                 |              |
A	  small	  %	  of	  the	  operational	  profile	  may	  account	  for
a	  large	  %	  of	  failures
32

|                      |     | Very   |         | high	  reliability |        |              |     |
| -------------------- | --- | ------ | ------- | ------------------- | ------ | ------------ | --- |
| Safety-­‐critical    |     |        | system: |                     |        |              |     |
| Failure              | can | harm   |         | or	  kill          | people |              |     |
| Airplane,	  nuclear |     |        |         | plant,	  medical   |        | device,	  … |     |
| Increasing           |     | amount |         | of	  software      |        |              |     |
| Demands              |     | very   | high    | reliability         |        |              |     |
Example:	  Airbus	  A320	  fly-­‐by-­‐wire
10-­‐9
|     | failures |     | per	  hour |     |     |     |     |
| --- | -------- | --- | ----------- | --- | --- | --- | --- |
=	  once	  per	  100	  000	  years
| Cannot | be          | tested |     | directly! |             |     |           |
| ------ | ----------- | ------ | --- | --------- | ----------- | --- | --------- |
| Ensure | reliability |        |     | through   | development |     | practices |
34

Diminishing Rates
Diminishing return: wait longer for the next fault
Not clear what the ultimate rate will be
35

Building Safety-­‐Critical Systems
Formal verification techniques
Loss in translating from natural language
Proofs are hard and may have errors
Design diversity
Same system with different teams and designs, voting
scheme
Examples: space shuttle, Airbus A320
Still common faults due to common techniques and
approaches
Dependence is very hard to estimate
36

Summary
| Principles | of	  reliability |     |     |     |     |
| ---------- | ----------------- | --- | --- | --- | --- |
Goal:	  predict reliability
| Failure | probability | distributions,	  MTTF |     |     |     |
| ------- | ----------- | ---------------------- | --- | --- | --- |
Software	  reliability
| Prediction | systems:	  future	  failure |     |     | times	  from | past |
| ---------- | ----------------------------- | --- | --- | ------------- | ---- |
Jelinski-­‐Moranda
| Statistical | testing,	  very |     | high	  reliability |     |     |
| ----------- | ---------------- | --- | ------------------- | --- | --- |
37

References
[FB] N.E. Fenton and J. Bieman. Software
Metrics: A Rigorous and Practical Approach. 3rd
edition, CRC Press, 2015.
Ch. 11
38