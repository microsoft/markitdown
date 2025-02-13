<?xml version='1.0' encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:m="http://www.w3.org/1998/Math/MathML"
                version='1.0'>
                
<!-- ====================================================================== -->
<!-- $id: tokens.xsl, 2002/22/11 Exp $
     This file is part of the XSLT MathML Library distribution.
     See ./README or http://www.raleigh.ru/MathML/mmltex for
     copyright and other information                                        -->
<!-- ====================================================================== -->

<xsl:template match="m:mi|m:mn|m:mo|m:mtext|m:ms">
	<xsl:call-template name="CommonTokenAtr"/>
</xsl:template>

<xsl:template name="mi">
	<xsl:choose>
		<xsl:when test="string-length(normalize-space(.))>1 and not(@mathvariant)">
			<xsl:text>\mathrm{</xsl:text>
				<xsl:apply-templates/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:otherwise>
			<xsl:apply-templates/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="mn">
	<xsl:apply-templates/>
</xsl:template>

<xsl:template name="mo">
	<xsl:apply-templates/>
</xsl:template>

<xsl:template name="mtext">
	<xsl:variable name="content">
		<xsl:call-template name="replaceMtextEntities">
			<xsl:with-param name="content" select="."/>
		</xsl:call-template>
	</xsl:variable>
	<xsl:text>\text{</xsl:text>
	<xsl:value-of select="$content"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="m:mspace">
	<xsl:text>\phantom{\rule</xsl:text>
	<xsl:if test="@depth">
		<xsl:text>[-</xsl:text>
		<xsl:value-of select="@depth"/>
		<xsl:text>]</xsl:text>
	</xsl:if>
	<xsl:text>{</xsl:text>
	<xsl:if test="not(@width)">
		<xsl:text>0ex</xsl:text>
	</xsl:if>
	<xsl:value-of select="@width"/>
	<xsl:text>}{</xsl:text>
	<xsl:if test="not(@height)">
		<xsl:text>0ex</xsl:text>
	</xsl:if>
	<xsl:value-of select="@height"/>
	<xsl:text>}}</xsl:text>
</xsl:template>

<xsl:template name="ms">
	<xsl:choose>
		<xsl:when test="@lquote"><xsl:value-of select="@lquote"/></xsl:when>
		<xsl:otherwise><xsl:text>"</xsl:text></xsl:otherwise>
	</xsl:choose><xsl:apply-templates/><xsl:choose>
		<xsl:when test="@rquote"><xsl:value-of select="@rquote"/></xsl:when>
		<xsl:otherwise><xsl:text>"</xsl:text></xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="CommonTokenAtr">
	<xsl:if test="@mathbackground">
		<xsl:text>\colorbox[rgb]{</xsl:text>
		<xsl:call-template name="color">
			<xsl:with-param name="color" select="@mathbackground"/>
		</xsl:call-template>
		<xsl:text>}{$</xsl:text>
	</xsl:if>
	<xsl:if test="@color or @mathcolor"> <!-- Note: @color is deprecated in MathML 2.0 -->
		<xsl:text>\textcolor[rgb]{</xsl:text>
		<xsl:call-template name="color">
			<xsl:with-param name="color" select="@color|@mathcolor"/>
		</xsl:call-template>
		<xsl:text>}{</xsl:text>
	</xsl:if>
	<xsl:if test="@mathvariant">
		<xsl:choose>
			<xsl:when test="@mathvariant='normal'">
				<xsl:text>\mathrm{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='bold'">
				<xsl:text>\mathbf{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='italic'">
				<xsl:text>\mathit{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='bold-italic'">	<!-- Required definition -->
				<xsl:text>\mathbit{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='double-struck'">	<!-- Required amsfonts -->
				<xsl:text>\mathbb{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='bold-fraktur'">	<!-- Error -->
				<xsl:text>{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='script'">
				<xsl:text>\mathcal{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='bold-script'">	<!-- Error -->
				<xsl:text>\mathsc{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='fraktur'">	<!-- Required amsfonts -->
				<xsl:text>\mathfrak{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='sans-serif'">
				<xsl:text>\mathsf{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='bold-sans-serif'"> <!-- Required definition -->
				<xsl:text>\mathbsf{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='sans-serif-italic'"> <!-- Required definition -->
				<xsl:text>\mathsfit{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='sans-serif-bold-italic'">	<!-- Error -->
				<xsl:text>\mathbsfit{</xsl:text>
			</xsl:when>
			<xsl:when test="@mathvariant='monospace'">
				<xsl:text>\mathtt{</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>{</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:if>
	<xsl:call-template name="selectTemplate"/>
	<xsl:if test="@mathvariant">
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:if test="@color or @mathcolor">
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:if test="@mathbackground">
		<xsl:text>$}</xsl:text>
	</xsl:if>
</xsl:template>

<xsl:template name="selectTemplate">
<!--	<xsl:variable name="name" select="local-name()"/>
	<xsl:call-template name="{$name}"/>-->
	<xsl:choose>
		<xsl:when test="local-name(.)='mi'">
			<xsl:call-template name="mi"/>
		</xsl:when>
		<xsl:when test="local-name(.)='mn'">
			<xsl:call-template name="mn"/>
		</xsl:when>
		<xsl:when test="local-name(.)='mo'">
			<xsl:call-template name="mo"/>
		</xsl:when>
		<xsl:when test="local-name(.)='mtext'">
			<xsl:call-template name="mtext"/>
		</xsl:when>
		<xsl:when test="local-name(.)='ms'">
			<xsl:call-template name="ms"/>
		</xsl:when>
	</xsl:choose>
</xsl:template>

<xsl:template name="color">
<!-- NB: Variables colora and valueColor{n} only for Sablotron -->
	<xsl:param name="color"/>
	<xsl:variable name="colora" select="translate($color,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
	<xsl:choose>
	<xsl:when test="starts-with($colora,'#') and string-length($colora)=4">
		<xsl:variable name="valueColor">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,2,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="$valueColor div 15"/><xsl:text>,</xsl:text>
		<xsl:variable name="valueColor1">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,3,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="$valueColor1 div 15"/><xsl:text>,</xsl:text>
		<xsl:variable name="valueColor2">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,4,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="$valueColor2 div 15"/>
	</xsl:when>
	<xsl:when test="starts-with($colora,'#') and string-length($colora)=7">
		<xsl:variable name="valueColor1">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,2,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="valueColor2">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,3,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="($valueColor1*16 + $valueColor2) div 255"/><xsl:text>,</xsl:text>
		<xsl:variable name="valueColor1a">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,4,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="valueColor2a">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,5,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="($valueColor1a*16 + $valueColor2a) div 255"/><xsl:text>,</xsl:text>
		<xsl:variable name="valueColor1b">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,6,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="valueColor2b">
			<xsl:call-template name="Hex2Decimal">
				<xsl:with-param name="arg" select="substring($colora,7,1)"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="($valueColor1b*16 + $valueColor2b) div 255"/>
	</xsl:when>
<!-- ======================= if color specifed as an html-color-name ========================================== -->
	<xsl:when test="$colora='aqua'"><xsl:text>0,1,1</xsl:text></xsl:when>
	<xsl:when test="$colora='black'"><xsl:text>0,0,0</xsl:text></xsl:when>
	<xsl:when test="$colora='blue'"><xsl:text>0,0,1</xsl:text></xsl:when>
	<xsl:when test="$colora='fuchsia'"><xsl:text>1,0,1</xsl:text></xsl:when>
	<xsl:when test="$colora='gray'"><xsl:text>.5,.5,.5</xsl:text></xsl:when>
	<xsl:when test="$colora='green'"><xsl:text>0,.5,0</xsl:text></xsl:when>
	<xsl:when test="$colora='lime'"><xsl:text>0,1,0</xsl:text></xsl:when>
	<xsl:when test="$colora='maroon'"><xsl:text>.5,0,0</xsl:text></xsl:when>
	<xsl:when test="$colora='navy'"><xsl:text>0,0,.5</xsl:text></xsl:when>
	<xsl:when test="$colora='olive'"><xsl:text>.5,.5,0</xsl:text></xsl:when>
	<xsl:when test="$colora='purple'"><xsl:text>.5,0,.5</xsl:text></xsl:when>
	<xsl:when test="$colora='red'"><xsl:text>1,0,0</xsl:text></xsl:when>
	<xsl:when test="$colora='silver'"><xsl:text>.75,.75,.75</xsl:text></xsl:when>
	<xsl:when test="$colora='teal'"><xsl:text>0,.5,.5</xsl:text></xsl:when>
	<xsl:when test="$colora='white'"><xsl:text>1,1,1</xsl:text></xsl:when>
	<xsl:when test="$colora='yellow'"><xsl:text>1,1,0</xsl:text></xsl:when>
	<xsl:otherwise>
		<xsl:message>Exception at color template</xsl:message>
	</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="Hex2Decimal">
	<xsl:param name="arg"/>
	<xsl:choose>
		<xsl:when test="$arg='f'">
			<xsl:value-of select="15"/>
		</xsl:when>
		<xsl:when test="$arg='e'">
			<xsl:value-of select="14"/>
		</xsl:when>
		<xsl:when test="$arg='d'">
			<xsl:value-of select="13"/>
		</xsl:when>
		<xsl:when test="$arg='c'">
			<xsl:value-of select="12"/>
		</xsl:when>
		<xsl:when test="$arg='b'">
			<xsl:value-of select="11"/>
		</xsl:when>
		<xsl:when test="$arg='a'">
			<xsl:value-of select="10"/>
		</xsl:when>
		<xsl:when test="translate($arg, '0123456789', '9999999999')='9'"> <!-- if $arg is number -->
			<xsl:value-of select="$arg"/>
		</xsl:when>
		<xsl:otherwise>
			<xsl:message>Exception at Hex2Decimal template</xsl:message>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="m:*/text()">
	<xsl:call-template name="replaceEntities">
		<xsl:with-param name="content" select="normalize-space()"/>
	</xsl:call-template>
</xsl:template>

</xsl:stylesheet>