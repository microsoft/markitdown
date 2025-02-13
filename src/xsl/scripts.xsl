<?xml version='1.0' encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:m="http://www.w3.org/1998/Math/MathML"
                version='1.0'>
                
<!-- ====================================================================== -->
<!-- $Id: scripts.xsl,v 1.1.1.1 2002/10/26 14:20:06 shade33 Exp $
     This file is part of the XSLT MathML Library distribution.
     See ./README or http://www.raleigh.ru/MathML/mmltex for
     copyright and other information                                        -->
<!-- ====================================================================== -->

<xsl:template match="m:munderover">
	<xsl:variable name="base">
		<xsl:call-template name="startspace">
			<xsl:with-param name="symbol" select="./*[1]"/>
		</xsl:call-template>
	</xsl:variable>
	<xsl:variable name="under">
		<xsl:call-template name="startspace">
			<xsl:with-param name="symbol" select="./*[2]"/>
		</xsl:call-template>
	</xsl:variable>
	<xsl:variable name="over">
		<xsl:call-template name="startspace">
			<xsl:with-param name="symbol" select="./*[3]"/>
		</xsl:call-template>
	</xsl:variable>
	
	<xsl:choose>
		<xsl:when test="$over='&#x000AF;'">	<!-- OverBar - over bar -->
			<xsl:text>\overline{</xsl:text>
			<xsl:call-template name="munder">
				<xsl:with-param name="base" select="$base"/>
				<xsl:with-param name="under" select="$under"/>
			</xsl:call-template>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="$over='&#x0FE37;'">	<!-- OverBrace - over brace -->
			<xsl:text>\overbrace{</xsl:text>
			<xsl:call-template name="munder">
				<xsl:with-param name="base" select="$base"/>
				<xsl:with-param name="under" select="$under"/>
			</xsl:call-template>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="$under='&#x00332;'">	<!-- UnderBar - combining low line -->
			<xsl:text>\underline{</xsl:text>
			<xsl:call-template name="mover">
				<xsl:with-param name="base" select="$base"/>
				<xsl:with-param name="over" select="$over"/>
				<xsl:with-param name="pos_over" select="3"/>
			</xsl:call-template>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="$under='&#x0FE38;'">	<!-- UnderBrace - under brace -->
			<xsl:text>\underbrace{</xsl:text>
			<xsl:call-template name="mover">
				<xsl:with-param name="base" select="$base"/>
				<xsl:with-param name="over" select="$over"/>
				<xsl:with-param name="pos_over" select="3"/>
			</xsl:call-template>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="translate($base,'&#x0220F;&#x02210;&#x022c2;&#x022c3;&#x02294;',
						'&#x02211;&#x02211;&#x02211;&#x02211;&#x02211;')='&#x02211;'">
<!-- if $base is operator, such as
			&#x02211;	/sum L: summation operator
			&#x0220F;	/prod L: product operator
			&#x02210;	/coprod L: coproduct operator
			&#x022c2;	/bigcap
			&#x022c3;	/bigcup
			&#x02294;	/bigsqcup
-->
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>_{</xsl:text>
			<xsl:apply-templates select="./*[2]"/>
			<xsl:text>}^{</xsl:text>
			<xsl:apply-templates select="./*[3]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:otherwise>
			<xsl:text>\underset{</xsl:text>
			<xsl:apply-templates select="./*[2]"/>
			<xsl:text>}{\overset{</xsl:text>
			<xsl:apply-templates select="./*[3]"/>
			<xsl:text>}{</xsl:text>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}}</xsl:text>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="m:mover">
	<xsl:call-template name="mover">
		<xsl:with-param name="base">
			<xsl:call-template name="startspace">
				<xsl:with-param name="symbol" select="./*[1]"/>
			</xsl:call-template>
		</xsl:with-param>
		<xsl:with-param name="over">
			<xsl:call-template name="startspace">
				<xsl:with-param name="symbol" select="./*[2]"/>
			</xsl:call-template>
		</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<xsl:template match="m:munder">
	<xsl:call-template name="munder">
		<xsl:with-param name="base">
			<xsl:call-template name="startspace">
				<xsl:with-param name="symbol" select="./*[1]"/>
			</xsl:call-template>
		</xsl:with-param>
		<xsl:with-param name="under">
			<xsl:call-template name="startspace">
				<xsl:with-param name="symbol" select="./*[2]"/>
			</xsl:call-template>
		</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<xsl:template name="mover">
	<xsl:param name="base"/>
	<xsl:param name="over"/>
	<xsl:param name="pos_over" select="2"/>
	<xsl:choose>
		<xsl:when test="$over='&#x000AF;'">	<!-- OverBar - over bar -->
			<xsl:text>\overline{</xsl:text>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="$over='&#x0FE37;'">	<!-- OverBrace - over brace -->
			<xsl:text>\overbrace{</xsl:text>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="translate($base,'&#x0220F;&#x02210;&#x022c2;&#x022c3;&#x02294;',
						'&#x02211;&#x02211;&#x02211;&#x02211;&#x02211;')='&#x02211;'">
<!-- if $base is operator, such as
			&#x02211;	/sum L: summation operator
			&#x0220F;	/prod L: product operator
			&#x02210;	/coprod L: coproduct operator
			&#x022c2;	/bigcap
			&#x022c3;	/bigcup
			&#x02294;	/bigsqcup
-->
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>^{</xsl:text>
			<xsl:apply-templates select="./*[$pos_over]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:otherwise>
			<xsl:text>\stackrel{</xsl:text>
			<xsl:apply-templates select="./*[$pos_over]"/>
			<xsl:text>}{</xsl:text>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>
			<!--
			<xsl:text>\overset{</xsl:text>
			<xsl:apply-templates select="./*[$pos_over]"/>
			<xsl:text>}{</xsl:text>	
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>-->
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="munder">
	<xsl:param name="base"/>
	<xsl:param name="under"/>
	<xsl:choose>
		<xsl:when test="$under='&#x00332;'">	<!-- UnderBar - combining low line -->
			<xsl:text>\underline{</xsl:text>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="$under='&#x0FE38;'">	<!-- UnderBrace - under brace -->
			<xsl:text>\underbrace{</xsl:text>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:when test="translate($base,'&#x0220F;&#x02210;&#x022c2;&#x022c3;&#x02294;',
						'&#x02211;&#x02211;&#x02211;&#x02211;&#x02211;')='&#x02211;'">
<!-- if $base is operator, such as
			&#x02211;	/sum L: summation operator
			&#x0220F;	/prod L: product operator
			&#x02210;	/coprod L: coproduct operator
			&#x022c2;	/bigcap
			&#x022c3;	/bigcup
			&#x02294;	/bigsqcup
-->
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>_{</xsl:text>
			<xsl:apply-templates select="./*[2]"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:otherwise>
			<xsl:text>\underset{</xsl:text>		<!-- Required AmsMath package -->
			<xsl:apply-templates select="./*[2]"/>
			<xsl:text>}{</xsl:text>	
			<xsl:apply-templates select="./*[1]"/>
			<xsl:text>}</xsl:text>	
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="m:msubsup">
	<xsl:text>{</xsl:text>	
	<xsl:apply-templates select="./*[1]"/>
	<xsl:text>}_{</xsl:text>
	<xsl:apply-templates select="./*[2]"/>
	<xsl:text>}^{</xsl:text>	
	<xsl:apply-templates select="./*[3]"/>
	<xsl:text>}</xsl:text>	
</xsl:template>

<xsl:template match="m:msup">
	<xsl:text>{</xsl:text>	
	<xsl:apply-templates select="./*[1]"/>
	<xsl:text>}^{</xsl:text>	
	<xsl:apply-templates select="./*[2]"/>
	<xsl:text>}</xsl:text>	
</xsl:template>

<xsl:template match="m:msub">
	<xsl:text>{</xsl:text>	
	<xsl:apply-templates select="./*[1]"/>
	<xsl:text>}_{</xsl:text>	
	<xsl:apply-templates select="./*[2]"/>
	<xsl:text>}</xsl:text>	
</xsl:template>

<xsl:template match="m:mmultiscripts" mode="mprescripts">
	<xsl:for-each select="m:mprescripts/following-sibling::*">
		<xsl:if test="position() mod 2 and local-name(.)!='none'">
			<xsl:text>{}_{</xsl:text>	
			<xsl:apply-templates select="."/>
			<xsl:text>}</xsl:text>	
		</xsl:if>
		<xsl:if test="not(position() mod 2) and local-name(.)!='none'">
			<xsl:text>{}^{</xsl:text>	
			<xsl:apply-templates select="."/>
			<xsl:text>}</xsl:text>	
		</xsl:if>
	</xsl:for-each>
	<xsl:apply-templates select="./*[1]"/>
	<xsl:for-each select="m:mprescripts/preceding-sibling::*[position()!=last()]">
		<xsl:if test="position()>2 and local-name(.)!='none'">
			<xsl:text>{}</xsl:text>	
		</xsl:if>
		<xsl:if test="position() mod 2 and local-name(.)!='none'">
			<xsl:text>_{</xsl:text>	
			<xsl:apply-templates select="."/>
			<xsl:text>}</xsl:text>	
		</xsl:if>
		<xsl:if test="not(position() mod 2) and local-name(.)!='none'">
			<xsl:text>^{</xsl:text>	
			<xsl:apply-templates select="."/>
			<xsl:text>}</xsl:text>	
		</xsl:if>
	</xsl:for-each>
</xsl:template>

<xsl:template match="m:mmultiscripts">
	<xsl:choose>
		<xsl:when test="m:mprescripts">
			<xsl:apply-templates select="." mode="mprescripts"/>
		</xsl:when>
		<xsl:otherwise>
			<xsl:apply-templates select="./*[1]"/>
			<xsl:for-each select="*[position()>1]">
				<xsl:if test="position()>2 and local-name(.)!='none'">
					<xsl:text>{}</xsl:text>	
				</xsl:if>
				<xsl:if test="position() mod 2 and local-name(.)!='none'">
					<xsl:text>_{</xsl:text>	
					<xsl:apply-templates select="."/>
					<xsl:text>}</xsl:text>	
				</xsl:if>
				<xsl:if test="not(position() mod 2) and local-name(.)!='none'">
					<xsl:text>^{</xsl:text>	
					<xsl:apply-templates select="."/>
					<xsl:text>}</xsl:text>	
				</xsl:if>
			</xsl:for-each>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

</xsl:stylesheet>