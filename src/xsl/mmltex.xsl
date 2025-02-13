<?xml version='1.0' encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:m="http://www.w3.org/1998/Math/MathML"
                version='1.0'>
                
<xsl:output method="text" indent="no" encoding="UTF-8"/>

<!-- ====================================================================== -->
<!-- $id: mmltex.xsl, 2002/22/11 Exp $
     This file is part of the XSLT MathML Library distribution.
     See ./README or http://www.raleigh.ru/MathML/mmltex for
     copyright and other information                                        -->
<!-- ====================================================================== -->

<xsl:include href="tokens.xsl"/>
<xsl:include href="glayout.xsl"/>
<xsl:include href="scripts.xsl"/>
<xsl:include href="tables.xsl"/>
<xsl:include href="entities.xsl"/>
<xsl:include href="cmarkup.xsl"/>

<!-- Note: variables colora (template color) and symbola (template startspace) only for Sablotron -->

<xsl:template name="startspace">
	<xsl:param name="symbol"/>
	<xsl:if test="contains($symbol,' ')">
		<xsl:variable name="symbola" select="concat(substring-before($symbol,' '),substring-after($symbol,' '))"/>
		<xsl:call-template name="startspace">
			<xsl:with-param name="symbol" select="$symbola"/>
		</xsl:call-template>
	</xsl:if>
	<xsl:if test="not(contains($symbol,' '))">
		<xsl:value-of select="$symbol"/>
	</xsl:if>
</xsl:template>

<xsl:strip-space elements="m:*"/>

<xsl:template match="m:math">
	<xsl:text>&#x00024;</xsl:text>
	<xsl:apply-templates/>
	<xsl:text>&#x00024;</xsl:text>
</xsl:template>

</xsl:stylesheet>