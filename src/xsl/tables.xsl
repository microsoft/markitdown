<?xml version='1.0' encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:m="http://www.w3.org/1998/Math/MathML"
                version='1.0'>
                
<!-- ====================================================================== -->
<!-- $id: tables.xsl, 2002/17/05 Exp $
     This file is part of the XSLT MathML Library distribution.
     See ./README or http://www.raleigh.ru/MathML/mmltex for
     copyright and other information                                        -->
<!-- ====================================================================== -->

<xsl:template match="m:mtd[@columnspan]">
	<xsl:text>\multicolumn{</xsl:text>
	<xsl:value-of select="@columnspan"/>
	<xsl:text>}{c}{</xsl:text>
	<xsl:apply-templates/>
	<xsl:text>}</xsl:text>
	<xsl:if test="count(following-sibling::*)>0">
		<xsl:text>&amp; </xsl:text>
	</xsl:if>
</xsl:template>


<xsl:template match="m:mtd">
	<xsl:if test="@columnalign='right' or @columnalign='center'">
		<xsl:text>\hfill </xsl:text>
	</xsl:if>
	<xsl:apply-templates/>
	<xsl:if test="@columnalign='left' or @columnalign='center'">
		<xsl:text>\hfill </xsl:text>
	</xsl:if>
	<xsl:if test="count(following-sibling::*)>0">
<!--    this test valid for Sablotron, another form - test="not(position()=last())".
	Also for m:mtd[@columnspan] and m:mtr  -->
		<xsl:text>&amp; </xsl:text>
	</xsl:if>
</xsl:template>

<xsl:template match="m:mtr">
	<xsl:apply-templates/>
	<xsl:if test="count(following-sibling::*)>0">
		<xsl:text>\\ </xsl:text>
	</xsl:if>
</xsl:template>

<xsl:template match="m:mtable">
	<xsl:text>\begin{array}{</xsl:text>
	<xsl:if test="@frame='solid'">
		<xsl:text>|</xsl:text>
	</xsl:if>
	<xsl:variable name="numbercols" select="count(./m:mtr[1]/m:mtd[not(@columnspan)])+sum(./m:mtr[1]/m:mtd/@columnspan)"/>
	<xsl:choose>
		<xsl:when test="@columnalign">
			<xsl:variable name="colalign">
				<xsl:call-template name="colalign">
					<xsl:with-param name="colalign" select="@columnalign"/>
				</xsl:call-template>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="string-length($colalign) > $numbercols">
					<xsl:value-of select="substring($colalign,1,$numbercols)"/>
				</xsl:when>
				<xsl:when test="string-length($colalign) &lt; $numbercols">
					<xsl:value-of select="$colalign"/>
					<xsl:call-template name="generate-string">
						<xsl:with-param name="text" select="substring($colalign,string-length($colalign))"/>
						<xsl:with-param name="count" select="$numbercols - string-length($colalign)"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$colalign"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:otherwise>
			<xsl:call-template name="generate-string">
				<xsl:with-param name="text" select="'c'"/>
				<xsl:with-param name="count" select="$numbercols"/>
			</xsl:call-template>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:if test="@frame='solid'">
		<xsl:text>|</xsl:text>
	</xsl:if>
	<xsl:text>}</xsl:text>
	<xsl:if test="@frame='solid'">
		<xsl:text>\hline </xsl:text>
	</xsl:if>
	<xsl:apply-templates/>
	<xsl:if test="@frame='solid'">
		<xsl:text>\\ \hline</xsl:text>
	</xsl:if>
	<xsl:text>\end{array}</xsl:text>
</xsl:template>

<xsl:template name="colalign">
	<xsl:param name="colalign"/>
	<xsl:choose>
		<xsl:when test="contains($colalign,' ')">
			<xsl:value-of select="substring($colalign,1,1)"/>
			<xsl:call-template name="colalign">
				<xsl:with-param name="colalign" select="substring-after($colalign,' ')"/>
			</xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="substring($colalign,1,1)"/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="generate-string">
<!-- template from XSLT Standard Library v1.1 -->
    <xsl:param name="text"/>
    <xsl:param name="count"/>

    <xsl:choose>
      <xsl:when test="string-length($text) = 0 or $count &lt;= 0"/>

      <xsl:otherwise>
	<xsl:value-of select="$text"/>
	<xsl:call-template name="generate-string">
	  <xsl:with-param name="text" select="$text"/>
	  <xsl:with-param name="count" select="$count - 1"/>
	</xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>