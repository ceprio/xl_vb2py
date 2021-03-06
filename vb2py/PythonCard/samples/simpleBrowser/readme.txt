simpleBrowser is not designed to be a full web browser.

The default URL is set to http://diveintopython.org/toc.html, but you can change that in the resource file.

Due to limitations in HtmlWindow and the underlying wxHtmlWindow class, both the HtmlWindow component and the simpleBrowser sample are likely to change a great deal between releases. wxHtmlWindow does not have event bindings, nor can you select the text in the control.

As of wxPython 2.3.2.1, the underlying wxHtmlWindow class does not send a Host: header to web servers, so servers expecting a full HTTP/1.1 request will generally return an error page. This includes almost all Apache servers, including SourceForge. The next version of wxHtmlWindow and wxPython should fix this problem so that the control works with more servers.

I recommend working with HTML files on your local system to avoid HTTP server issues.

The control does not support frames, JavaScript, and many other more advanced HTML features. A list of supported tags is below. Just try it with files on your local system to see what does and doesn't work. I think that it does give us a very simple way to do non-editable styled text with embedded images, tables, etc. and this is the area I would like to explore. It is not going to give us the power of Mozilla or the Internet Explorer ActiveX control.

The underlying wxHtmlWindow control does support embedding other wxWindows classes in HTML and while this is fairly advanced, it is also very powerful. See the wxPython demo.py for an example. We should keep this in mind as the framework progresses.

See the wxWindows/wxPython help file for more info on HTML classes.

---------------------------------------------------------------------------

Tags supported by wxHTML
wxHTML is not full implementation of HTML standard. Instead, it supports
most common tags so that it is possible to display simple HTML documents
with it. (For example it works fine with pages created in Netscape Composer
or generated by tex2rtf).

Following tables list all tags known to wxHTML, together with supported
parameters. A tag has general form of <tagname param_1 param_2 ... param_n>
where param_i is either paramname="paramvalue" or paramname=paramvalue -
these two are equivalent. Unless stated otherwise, wxHTML is
case-insensitive.

Table of common parameter values

We will use these substitutions in tags descriptions:


[alignment]     CENTER
                LEFT
                RIGHT
                JUSTIFY

[v_alignment]   TOP
                BOTTOM
                CENTER

[color]         HTML 4.0-compliant colour specification

[fontsize]      -2
                -1
                +0
                +1
                +2
                +3
                +4
                 1
                 2
                 3
                 4
                 5
                 6
                 7

[pixels]        integer value that represents dimension in pixels

[percent]       i%
                where i is integer

[url]           an URL

[string]        text string

[coords]        c(1),c(2),c(3),...,c(n)
                where c(i) is integer


List of supported tags

A               NAME=[string]
                HREF=[url]
                TARGET=[target window spec]
ADDRESS
AREA            SHAPE=POLY
                SHAPE=CIRCLE
                SHAPE=RECT
                COORDS=[coords]
                HREF=[url]
B
BIG
BLOCKQUOTE
BODY            TEXT=[color]
                LINK=[color]
                BGCOLOR=[color]
BR              ALIGN=[alignment]
CENTER
CITE
CODE
DD
DIV             ALIGN=[alignment]
DL
DT
EM
FONT            COLOR=[color]
                SIZE=[fontsize]
                FACE=[comma-separated list of facenames]
HR              ALIGN=[alignment]
                SIZE=[pixels]
                WIDTH=[percent|pixels]
                NOSHADE
H1
H2
H3
H4
H5
H6
I
IMG             SRC=[url]
                WIDTH=[pixels]
                HEIGHT=[pixels]
                ALIGN=TEXTTOP
                ALIGN=CENTER
                ALIGN=ABSCENTER
                ALIGN=BOTTOM
                USEMAP=[url]
KBD
LI
MAP             NAME=[string]
META            HTTP-EQUIV="Content-Type"
                CONTENT=[string]
OL
P               ALIGN=[alignment]
PRE
SAMP
SMALL
STRIKE
STRONG
TABLE           ALIGN=[alignment]
                WIDTH=[percent|pixels]
                BORDER=[pixels]
                VALIGN=[v_alignment]
                BGCOLOR=[color]
                CELLSPACING=[pixels]
                CELLPADDING=[pixels]
TD              ALIGN=[alignment]
                VALIGN=[v_alignment]
                BGCOLOR=[color]
                WIDTH=[percent|pixels]
                COLSPAN=[pixels]
                ROWSPAN=[pixels]
TH              ALIGN=[alignment]
                VALIGN=[v_alignment]
                BGCOLOR=[color]
                WIDTH=[percent|pixels]
                COLSPAN=[pixels]
                ROWSPAN=[pixels]
TITLE
TR              ALIGN=[alignment]
                VALIGN=[v_alignment]
                BGCOLOR=[color]
TT
U
UL
