<?xml version='1.0' encoding="UTF-8"?>
<xsl:stylesheet
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:m="http://www.w3.org/1998/Math/MathML"
		version='1.0'>
                
<!-- ====================================================================== -->
<!-- $id: tokens.xsl, 2002/22/11 Exp $
     This file is part of the XSLT MathML Library distribution.
     See ./README or http://www.raleigh.ru/MathML/mmltex for
     copyright and other information                                        -->
<!-- ====================================================================== -->

<!-- 4.4.1.1 cn -->
<xsl:template match="m:cn"><xsl:apply-templates/></xsl:template>

<xsl:template match="m:cn[@type='complex-cartesian']">
	<xsl:apply-templates select="text()[1]"/>
  	<xsl:text>+</xsl:text>
	<xsl:apply-templates select="text()[2]"/>
	<xsl:text>i</xsl:text>
</xsl:template>

<xsl:template match="m:cn[@type='rational']">
	<xsl:apply-templates select="text()[1]"/>
	<xsl:text>/</xsl:text>
	<xsl:apply-templates select="text()[2]"/>
</xsl:template>

<xsl:template match="m:cn[@type='integer' and @base!=10]">
		<xsl:apply-templates/>
		<xsl:text>_{</xsl:text><xsl:value-of select="@base"/><xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="m:cn[@type='complex-polar']">
	<xsl:apply-templates select="text()[1]"/>
	<xsl:text>e^{i </xsl:text>
	<xsl:apply-templates select="text()[2]"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="m:cn[@type='e-notation']">
    <xsl:apply-templates select="text()[1]"/>
    <xsl:text>E</xsl:text>
    <xsl:apply-templates select="text()[2]"/>
</xsl:template>

<!-- 4.4.1.1 ci 4.4.1.2 csymbol -->
<xsl:template match="m:ci | m:csymbol">
	<xsl:choose>
		<xsl:when test="string-length(normalize-space(text()))>1">
			<xsl:text>\mathrm{</xsl:text><xsl:apply-templates/><xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- 4.4.2.1 apply 4.4.2.2 reln -->
<xsl:template match="m:apply | m:reln">
	<xsl:apply-templates select="*[1]">
	<!-- <? -->
		<xsl:with-param name="p" select="10"/>
	</xsl:apply-templates>
	<!-- ?> -->
 	<xsl:text>(</xsl:text>
	<xsl:for-each select="*[position()>1]">
		<xsl:apply-templates select="."/>
		<xsl:if test="not(position()=last())"><xsl:text>, </xsl:text></xsl:if>
	</xsl:for-each>
 	<xsl:text>)</xsl:text>
</xsl:template>

<!-- 4.4.2.3 fn -->
<xsl:template match="m:fn[m:apply[1]]"> <!-- for m:fn using default rule -->
	<xsl:text>(</xsl:text><xsl:apply-templates/><xsl:text>)</xsl:text>
</xsl:template>

<!-- 4.4.2.4 interval -->
<xsl:template match="m:interval[*[2]]">
	<xsl:choose>
		<xsl:when test="@closure='open' or @closure='open-closed'">
			<xsl:text>\left(</xsl:text>		
		</xsl:when>
		<xsl:otherwise><xsl:text>\left[</xsl:text></xsl:otherwise> 
	</xsl:choose>
	<xsl:apply-templates select="*[1]"/>
	<xsl:text> , </xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:choose>
		<xsl:when test="@closure='open' or @closure='closed-open'">
			<xsl:text>\right)</xsl:text>		
		</xsl:when>
		<xsl:otherwise><xsl:text>\right]</xsl:text></xsl:otherwise> 
	</xsl:choose>
</xsl:template>

<xsl:template match="m:interval">
	<xsl:text>\left\{</xsl:text><xsl:apply-templates/><xsl:text>\right\}</xsl:text>
</xsl:template>

<!-- 4.4.2.5 inverse -->
<xsl:template match="m:apply[*[1][self::m:inverse]]">
	<xsl:apply-templates select="*[2]"/><xsl:text>^{(-1)}</xsl:text>
</xsl:template>

<!-- 4.4.2.6 sep 4.4.2.7 condition -->
<xsl:template match="m:sep | m:condition"><xsl:apply-templates/></xsl:template>

<!-- 4.4.2.9 lambda -->
<xsl:template match="m:lambda">
	<xsl:text>\mathrm{lambda}\: </xsl:text>
  	<xsl:apply-templates select="m:bvar/*"/>
  	<xsl:text>.\: </xsl:text>
  <xsl:apply-templates select="*[last()]"/>
</xsl:template>

<!-- 4.4.2.10 compose -->
<xsl:template match="m:apply[*[1][self::m:compose]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\circ </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.2.11 ident -->
<xsl:template match="m:ident"><xsl:text>\mathrm{id}</xsl:text></xsl:template>

<!-- 4.4.2.12 domain 4.4.2.13 codomain 4.4.2.14 image 4.4.3.21 arg 4.4.3.24 lcm
		4.4.5.9 grad 4.4.5.10 curl 4.4.9.4 median 4.4.9.5 mode-->
<xsl:template match="m:domain | m:codomain | m:image | m:arg | m:lcm | m:grad |
								 m:curl | m:median | m:mode">
	<xsl:text>\mathop{\mathrm{</xsl:text>
	<xsl:value-of select="local-name()"/>
	<xsl:text>}}</xsl:text>
</xsl:template>

<!-- 4.4.2.15 domainofapplication -->
<xsl:template match="m:domainofapplication"/>

<!-- 4.4.2.16 piecewise -->
<xsl:template match="m:piecewise">
	<xsl:text>\begin{cases}</xsl:text>
	<xsl:apply-templates select="m:piece"/>
	<xsl:apply-templates select="m:otherwise"/>
	<xsl:text>\end{cases}</xsl:text>
</xsl:template>

<xsl:template match="m:piece">
		<xsl:apply-templates select="*[1]"/>
		<xsl:text> &amp; \text{if $</xsl:text>
		<xsl:apply-templates select="*[2]"/>
		<xsl:text>$}</xsl:text>
		<xsl:if test="not(position()=last()) or ../m:otherwise"><xsl:text>\\ </xsl:text></xsl:if>
</xsl:template>

<xsl:template match="m:otherwise">
	<xsl:apply-templates select="*[1]"/>
	<xsl:text> &amp; \text{otherwise}</xsl:text>
</xsl:template>

<!-- 4.4.3.1 quotient -->
<xsl:template match="m:apply[*[1][self::m:quotient]]">
	<xsl:text>\left\lfloor\frac{</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>}{</xsl:text>
	<xsl:apply-templates select="*[3]"/>
	<xsl:text>}\right\rfloor </xsl:text>
</xsl:template>

<!-- 4.4.3.2 factorial -->
<xsl:template match="m:apply[*[1][self::m:factorial]]">
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
	<xsl:text>!</xsl:text>
</xsl:template>

<!-- 4.4.3.3 divide -->
<xsl:template match="m:apply[*[1][self::m:divide]]">
	<xsl:param name="p" select="0"/>
  <xsl:param name="this-p" select="3"/>
  <xsl:if test="$this-p &lt; $p"><xsl:text>\left(</xsl:text></xsl:if>
  <xsl:text>\frac{</xsl:text>
	<xsl:apply-templates select="*[2]"/>
<!--		<xsl:with-param name="p" select="$this-p"/>
	</xsl:apply-templates>-->
	<xsl:text>}{</xsl:text>
	<xsl:apply-templates select="*[3]"/>
<!--    	<xsl:with-param name="p" select="$this-p"/>
	</xsl:apply-templates>-->
	<xsl:text>}</xsl:text>
	<xsl:if test="$this-p &lt; $p"><xsl:text>\right)</xsl:text></xsl:if>
</xsl:template>

<!-- 4.4.3.4 max min -->
<xsl:template match="m:apply[*[1][self::m:max or self::m:min]]">
	<xsl:text>\</xsl:text>
	<xsl:value-of select="local-name(*[1])"/>
	<xsl:text>\{</xsl:text>
   <xsl:choose>
		<xsl:when test="m:condition">
   		<xsl:apply-templates select="*[last()]"/>
   		<xsl:text>, </xsl:text>
			<xsl:apply-templates select="m:condition/node()"/>
		</xsl:when>
		<xsl:otherwise>
			<xsl:for-each select="*[position() &gt; 1]">
				<xsl:apply-templates select="."/>
				<xsl:if test="position() !=last()"><xsl:text> , </xsl:text></xsl:if>
			</xsl:for-each>
		</xsl:otherwise>
   </xsl:choose>
	<xsl:text>\}</xsl:text>
</xsl:template>

<!-- 4.4.3.5  minus-->
<xsl:template match="m:apply[*[1][self::m:minus] and count(*)=2]">
	<xsl:text>-</xsl:text>
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="5"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="m:apply[*[1][self::m:minus] and count(*)&gt;2]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="mo">-</xsl:with-param>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="this-p" select="2"/>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.3.6  plus-->
<xsl:template match="m:apply[*[1][self::m:plus]]">
  <xsl:param name="p" select="0"/>
  <xsl:if test="$p &gt; 2">
		<xsl:text>(</xsl:text>
	</xsl:if>
  <xsl:for-each select="*[position()&gt;1]">
   <xsl:if test="position() &gt; 1">
    <xsl:choose>
      <xsl:when test="self::m:apply[*[1][self::m:times] and
      *[2][self::m:apply/*[1][self::m:minus] or self::m:cn[not(m:sep) and
      (number(.) &lt; 0)]]]">-</xsl:when>
      <xsl:otherwise>+</xsl:otherwise>
    </xsl:choose>
   </xsl:if>   
    <xsl:choose>
      <xsl:when test="self::m:apply[*[1][self::m:times] and
      *[2][self::m:cn[not(m:sep) and (number(.) &lt;0)]]]">
			<xsl:value-of select="-(*[2])"/>
			<xsl:apply-templates select=".">
		     <xsl:with-param name="first" select="2"/>
		     <xsl:with-param name="p" select="2"/>
		   </xsl:apply-templates>
       </xsl:when>
      <xsl:when test="self::m:apply[*[1][self::m:times] and
      *[2][self::m:apply/*[1][self::m:minus]]]">
				<xsl:apply-templates select="./*[2]/*[2]"/>
				<xsl:apply-templates select=".">
					<xsl:with-param name="first" select="2"/>
					<xsl:with-param name="p" select="2"/>
				</xsl:apply-templates>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select=".">
					<xsl:with-param name="p" select="2"/>
				</xsl:apply-templates>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
	<xsl:if test="$p &gt; 2">
		<xsl:text>)</xsl:text>
	</xsl:if>
</xsl:template>

<!-- 4.4.3.7 power -->
<xsl:template match="m:apply[*[1][self::m:power]]">
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="5"/>
	</xsl:apply-templates>
	<xsl:text>^{</xsl:text>
	<xsl:apply-templates select="*[3]">
		<xsl:with-param name="p" select="5"/>
	</xsl:apply-templates>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.3.8 remainder -->
<xsl:template match="m:apply[*[1][self::m:rem]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="mo">\mod </xsl:with-param>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="this-p" select="3"/>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.3.9  times-->
<xsl:template match="m:apply[*[1][self::m:times]]" name="times">
  <xsl:param name="p" select="0"/>
  <xsl:param name="first" select="1"/>
  <xsl:if test="$p &gt; 3"><xsl:text>(</xsl:text></xsl:if>
  <xsl:for-each select="*[position()&gt;1]">
		<xsl:if test="position() &gt; 1">
			<xsl:choose>
				<xsl:when test="self::m:cn">\times <!-- times --></xsl:when>
				<xsl:otherwise><!--invisible times--></xsl:otherwise>
			</xsl:choose>
		</xsl:if> 
		<xsl:if test="position()&gt;= $first">
			<xsl:apply-templates select=".">
				<xsl:with-param name="p" select="3"/>
			</xsl:apply-templates>
		</xsl:if>
	</xsl:for-each>
  <xsl:if test="$p &gt; 3"><xsl:text>)</xsl:text></xsl:if>
</xsl:template>

<!-- 4.4.3.10 root -->
<xsl:template match="m:apply[*[1][self::m:root]]">
	<xsl:text>\sqrt</xsl:text>
	<xsl:if test="m:degree!=2">
		<xsl:text>[</xsl:text>
		<xsl:apply-templates select="m:degree/*"/>
		<xsl:text>]</xsl:text>
	</xsl:if>
	<xsl:text>{</xsl:text>
	<xsl:apply-templates select="*[position()&gt;1 and not(self::m:degree)]"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.3.11 gcd -->
<xsl:template match="m:gcd"><xsl:text>\gcd </xsl:text></xsl:template>

<!-- 4.4.3.12 and -->
<xsl:template match="m:apply[*[1][self::m:and]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\land <!-- and --></xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.3.13 or -->
<xsl:template match="m:apply[*[1][self::m:or]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="3"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\lor </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.3.14 xor -->
<xsl:template match="m:apply[*[1][self::m:xor]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="3"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\mathop{\mathrm{xor}}</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.3.15 not -->
<xsl:template match="m:apply[*[1][self::m:not]]">
	<xsl:text>\neg </xsl:text>
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
</xsl:template>

<!-- 4.4.3.16 implies -->
<xsl:template match="m:apply[*[1][self::m:implies]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="mo">\implies </xsl:with-param>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="this-p" select="3"/>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.3.17 forall 4.4.3.18 exists -->
<xsl:template match="m:apply[*[1][self::m:forall or self::m:exists]]">
	<xsl:text>\</xsl:text>
	<xsl:value-of select="local-name(*[1])"/>
	<xsl:text> </xsl:text>
	<xsl:apply-templates select="m:bvar"/>
	<xsl:if test="m:condition">
		<xsl:text>, </xsl:text><xsl:apply-templates select="m:condition"/>
	</xsl:if>
	<xsl:if test="*[last()][local-name()!='condition'][local-name()!='bvar']">
		<xsl:text>\colon </xsl:text>
	  <xsl:apply-templates select="*[last()]"/>
  </xsl:if>
</xsl:template>

<!-- 4.4.3.19 abs -->
<xsl:template match="m:apply[*[1][self::m:abs]]">
	<xsl:text>\left|</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>\right|</xsl:text>
</xsl:template>

<!-- 4.4.3.20 conjugate -->
<xsl:template match="m:apply[*[1][self::m:conjugate]]">
	<xsl:text>\overline{</xsl:text><xsl:apply-templates select="*[2]"/><xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.3.22 real -->
<xsl:template match="m:real"><xsl:text>\Re </xsl:text></xsl:template>

<!-- 4.4.3.23 imaginary -->
<xsl:template match="m:imaginary"><xsl:text>\Im </xsl:text></xsl:template>

<!-- 4.4.3.25 floor -->
<xsl:template match="m:apply[*[1][self::m:floor]]">
	<xsl:text>\lfloor </xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>\rfloor </xsl:text>
</xsl:template>

<!-- 4.4.3.25 ceiling -->
<xsl:template match="m:apply[*[1][self::m:ceiling]]">
	<xsl:text>\lceil </xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>\rceil </xsl:text>
</xsl:template>

<!-- 4.4.4.1 eq -->
<xsl:template match="m:apply[*[1][self::m:eq]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">=</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.4.2 neq -->
<xsl:template match="m:apply[*[1][self::m:neq]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\neq </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.4.3 gt -->
<xsl:template match="m:apply[*[1][self::m:gt]]">
<xsl:param name="p" select="0"/>
<xsl:call-template name="infix">
	<xsl:with-param name="this-p" select="1"/>
	<xsl:with-param name="p" select="$p"/>
	<xsl:with-param name="mo">&gt; </xsl:with-param>
</xsl:call-template>
</xsl:template>

<!-- 4.4.4.4 lt -->
<xsl:template match="m:apply[*[1][self::m:lt]]">
<xsl:param name="p" select="0"/>
<xsl:call-template name="infix">
	<xsl:with-param name="this-p" select="1"/>
	<xsl:with-param name="p" select="$p"/>
	<xsl:with-param name="mo">&lt; </xsl:with-param>
</xsl:call-template>
</xsl:template>

<!-- 4.4.4.5 geq -->
<xsl:template match="m:apply[*[1][self::m:geq]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\ge </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.4.6 leq -->
<xsl:template match="m:apply[*[1][self::m:leq]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\le </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.4.7 equivalent -->
<xsl:template match="m:apply[*[1][self::m:equivalent]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\equiv </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.4.8 approx -->
<xsl:template match="m:apply[*[1][self::m:approx]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="1"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\approx </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.4.9 factorof -->
<xsl:template match="m:apply[*[1][self::m:factorof]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="mo"> | </xsl:with-param>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="this-p" select="3"/>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.5.1 int -->
<xsl:template match="m:apply[*[1][self::m:int]]">
	<xsl:text>\int</xsl:text>
	<xsl:if test="m:lowlimit/*|m:interval/*[1]|m:condition/*">
		<xsl:text>_{</xsl:text>
		<xsl:apply-templates select="m:lowlimit/*|m:interval/*[1]|m:condition/*"/>
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:if test="m:uplimit/*|m:interval/*[2]">
		<xsl:text>^{</xsl:text>
		<xsl:apply-templates select="m:uplimit/*|m:interval/*[2]"/>
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:text> </xsl:text>
	<xsl:apply-templates select="*[last()]"/>
	<xsl:text>\,d </xsl:text>
	<xsl:apply-templates select="m:bvar"/>
</xsl:template>

<!-- 4.4.5.2 diff -->
<xsl:template match="m:apply[*[1][self::m:diff] and m:ci and count(*)=2]" priority="2">
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>^\prime </xsl:text>
</xsl:template>

<xsl:template match="m:apply[*[1][self::m:diff]]" priority="1">
	<xsl:text>\frac{</xsl:text>
	<xsl:choose>
		<xsl:when test="m:bvar/m:degree">
			<xsl:text>d^{</xsl:text>
			<xsl:apply-templates select="m:bvar/m:degree/node()"/>
			<xsl:text>}</xsl:text>
			<xsl:apply-templates select="*[last()]"/>
			<xsl:text>}{d</xsl:text>
			<xsl:apply-templates select="m:bvar/node()"/>
			<xsl:text>^{</xsl:text>
			<xsl:apply-templates select="m:bvar/m:degree/node()"/>
			<xsl:text>}</xsl:text>
		</xsl:when>
		<xsl:otherwise>
			<xsl:text>d </xsl:text>
			<xsl:apply-templates select="*[last()]"/>
			<xsl:text>}{d </xsl:text>
			<xsl:apply-templates select="m:bvar"/>
			<xsl:text>}</xsl:text>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.5.3 partialdiff -->
<xsl:template match="m:apply[*[1][self::m:partialdiff] and m:list and m:ci and count(*)=3]" priority="2">
	<xsl:text>D_{</xsl:text>
	<xsl:for-each select="m:list[1]/*">
		<xsl:apply-templates select="."/>
		<xsl:if test="position()&lt;last()"><xsl:text>, </xsl:text></xsl:if>
	</xsl:for-each>
	<xsl:text>}</xsl:text>
	<xsl:apply-templates select="*[3]"/>
</xsl:template>

<xsl:template match="m:apply[*[1][self::m:partialdiff]]" priority="1">
	<xsl:text>\frac{\partial^{</xsl:text>
	<xsl:choose>
		<xsl:when test="m:degree">
			<xsl:apply-templates select="m:degree/node()"/>
		</xsl:when>
		<xsl:when test="m:bvar/m:degree[string(number(.))='NaN']">
			<xsl:for-each select="m:bvar/m:degree">
				<xsl:apply-templates select="node()"/>
				<xsl:if test="position()&lt;last()"><xsl:text>+</xsl:text></xsl:if>
			</xsl:for-each>
			<xsl:if test="count(m:bvar[not(m:degree)])&gt;0">
				<xsl:text>+</xsl:text>
				<xsl:value-of select="count(m:bvar[not(m:degree)])"/>
			</xsl:if>
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="sum(m:bvar/m:degree)+count(m:bvar[not(m:degree)])"/>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:text>}</xsl:text>
	<xsl:apply-templates select="*[last()]"/>
	<xsl:text>}{</xsl:text>
	<xsl:for-each select="m:bvar">
		<xsl:text>\partial </xsl:text>
		<xsl:apply-templates select="node()"/>
		<xsl:if test="m:degree">
			<xsl:text>^{</xsl:text>
			<xsl:apply-templates select="m:degree/node()"/>
			<xsl:text>}</xsl:text>
		</xsl:if>
	</xsl:for-each>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.2.8 declare 4.4.5.4 lowlimit 4.4.5.5 uplimit 4.4.5.7 degree 4.4.9.5 momentabout -->
<xsl:template match="m:declare | m:lowlimit | m:uplimit | m:degree | m:momentabout"/>

<!-- 4.4.5.6  bvar-->
<xsl:template match="m:bvar">
	<xsl:apply-templates/>
	<xsl:if test="following-sibling::m:bvar"><xsl:text>, </xsl:text></xsl:if>
</xsl:template>

<!-- 4.4.5.8 divergence-->
<xsl:template match="m:divergence"><xsl:text>\mathop{\mathrm{div}}</xsl:text></xsl:template>

<!-- 4.4.5.11 laplacian-->
<xsl:template match="m:laplacian"><xsl:text>\nabla^2 </xsl:text></xsl:template>

<!-- 4.4.6.1 set -->
<xsl:template match="m:set">
	<xsl:text>\{</xsl:text><xsl:call-template name="set"/><xsl:text>\}</xsl:text>
</xsl:template>

<!-- 4.4.6.2 list -->
<xsl:template match="m:list">
	<xsl:text>\left[</xsl:text><xsl:call-template name="set"/><xsl:text>\right]</xsl:text>
</xsl:template>

<xsl:template name="set">
   <xsl:choose>
		<xsl:when test="m:condition">
   		<xsl:apply-templates select="m:bvar/*[not(self::bvar or self::condition)]"/>
   		<xsl:text>\colon </xsl:text>
			<xsl:apply-templates select="m:condition/node()"/>
		</xsl:when>
		<xsl:otherwise>
			<xsl:for-each select="*">
				<xsl:apply-templates select="."/>
				<xsl:if test="position()!=last()"><xsl:text>, </xsl:text></xsl:if>
			</xsl:for-each>
		</xsl:otherwise>
   </xsl:choose>
</xsl:template>

<!-- 4.4.6.3 union -->
<xsl:template match="m:apply[*[1][self::m:union]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\cup </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.4 intersect -->
<xsl:template match="m:apply[*[1][self::m:intersect]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="3"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\cap </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.5 in -->
<xsl:template match="m:apply[*[1][self::m:in]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="mo">\in </xsl:with-param>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="this-p" select="3"/>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.5 notin -->
<xsl:template match="m:apply[*[1][self::m:notin]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="mo">\notin </xsl:with-param>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="this-p" select="3"/>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.7 subset -->
<xsl:template match="m:apply[*[1][self::m:subset]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\subseteq </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.8 prsubset -->
<xsl:template match="m:apply[*[1][self::m:prsubset]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\subset </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.9 notsubset -->
<xsl:template match="m:apply[*[1][self::m:notsubset]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\nsubseteq </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.10 notprsubset -->
<xsl:template match="m:apply[*[1][self::m:notprsubset]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\not\subset </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.11 setdiff -->
<xsl:template match="m:apply[*[1][self::m:setdiff]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\setminus </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.6.12 card -->
<xsl:template match="m:apply[*[1][self::m:card]]">
	<xsl:text>|</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>|</xsl:text>
</xsl:template>

<!-- 4.4.6.13 cartesianproduct 4.4.10.6 vectorproduct -->
<xsl:template match="m:apply[*[1][self::m:cartesianproduct or self::m:vectorproduct]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\times </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<xsl:template
match="m:apply[*[1][self::m:cartesianproduct][count(following-sibling::m:reals)=count(following-sibling::*)]]"
priority="2">
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="5"/>
	</xsl:apply-templates>
	<xsl:text>^{</xsl:text>
	<xsl:value-of select="count(*)-1"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.7.1 sum -->
<xsl:template match="m:apply[*[1][self::m:sum]]">
	<xsl:text>\sum</xsl:text><xsl:call-template name="series"/>
</xsl:template>

<!-- 4.4.7.2 product -->
<xsl:template match="m:apply[*[1][self::m:product]]">
	<xsl:text>\prod</xsl:text><xsl:call-template name="series"/>
</xsl:template>
	
<xsl:template name="series">
	<xsl:if test="m:lowlimit/*|m:interval/*[1]|m:condition/*">
		<xsl:text>_{</xsl:text>
		<xsl:if test="not(m:condition)">
			<xsl:apply-templates select="m:bvar"/>
			<xsl:text>=</xsl:text>
		</xsl:if>
		<xsl:apply-templates select="m:lowlimit/*|m:interval/*[1]|m:condition/*"/>
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:if test="m:uplimit/*|m:interval/*[2]">
		<xsl:text>^{</xsl:text>
		<xsl:apply-templates select="m:uplimit/*|m:interval/*[2]"/>
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:text> </xsl:text>
	<xsl:apply-templates select="*[last()]"/>
</xsl:template>

<!-- 4.4.7.3 limit -->
<xsl:template match="m:apply[*[1][self::m:limit]]">
	<xsl:text>\lim_{</xsl:text>
	<xsl:apply-templates select="m:lowlimit|m:condition/*"/>
	<xsl:text>}</xsl:text>
	<xsl:apply-templates select="*[last()]"/>
</xsl:template>

<xsl:template match="m:apply[m:limit]/m:lowlimit" priority="3">
	<xsl:apply-templates select="../m:bvar/node()"/>
	<xsl:text>\to </xsl:text>
	<xsl:apply-templates/>
</xsl:template>

<!-- 4.4.7.4 tendsto -->
<xsl:template match="m:apply[*[1][self::m:tendsto]]">
	<xsl:param name="p"/>
	<xsl:call-template name="binary">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">
			<xsl:choose>
				<xsl:when test="@type='above'">\searrow </xsl:when>
				<xsl:when test="@type='below'">\nearrow </xsl:when>
				<xsl:when test="@type='two-sided'">\rightarrow </xsl:when>
				<xsl:otherwise>\to </xsl:otherwise>
			</xsl:choose>
		</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.8.1 common tringonometric functions 4.4.8.3 natural logarithm -->
<xsl:template match="m:apply[*[1][
 self::m:sin or 		self::m:cos or 	self::m:tan or		self::m:sec or
 self::m:csc or 		self::m:cot or 	self::m:sinh or	 	self::m:cosh or
 self::m:tanh or 		self::m:coth or	self::m:arcsin or 	self::m:arccos or
 self::m:arctan or 	self::m:ln]]">
	<xsl:text>\</xsl:text>
	<xsl:value-of select="local-name(*[1])"/>
	<xsl:text> </xsl:text>
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="m:sin | m:cos | m:tan | m:sec | m:csc |
								 m:cot | m:sinh | m:cosh | m:tanh | m:coth |
								 m:arcsin | m:arccos | m:arctan | m:ln">
	<xsl:text>\</xsl:text>
	<xsl:value-of select="local-name(.)"/>
	<xsl:text> </xsl:text>
</xsl:template>

<xsl:template match="m:apply[*[1][
 self::m:sech or 		self::m:csch or		self::m:arccosh or
 self::m:arccot or 	self::m:arccoth or 	self::m:arccsc or
 self::m:arccsch or self::m:arcsec or 	self::m:arcsech or
 self::m:arcsinh or self::m:arctanh]]">
	<xsl:text>\mathrm{</xsl:text>
	<xsl:value-of select="local-name(*[1])"/>
	<xsl:text>\,}</xsl:text>
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="m:sech | m:csch | m:arccosh | m:arccot |
								 m:arccoth | m:arccsc |m:arccsch |m:arcsec |
								 m:arcsech | m:arcsinh | m:arctanh">
	<xsl:text>\mathrm{</xsl:text>
	<xsl:value-of select="local-name(.)"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.8.2 exp -->
<xsl:template match="m:apply[*[1][self::m:exp]]">
	<xsl:text>e^{</xsl:text><xsl:apply-templates select="*[2]"/><xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.8.4 log -->
<xsl:template match="m:apply[*[1][self::m:log]]">
	<xsl:text>\lg </xsl:text>
	<xsl:apply-templates select="*[last()]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="m:apply[*[1][self::m:log] and m:logbase != 10]">
	<xsl:text>\log_{</xsl:text>
	<xsl:apply-templates select="m:logbase/node()"/>
	<xsl:text>}</xsl:text>
	<xsl:apply-templates select="*[last()]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
</xsl:template>

<!-- 4.4.9.1 mean -->
<xsl:template match="m:apply[*[1][self::m:mean]]">
	<xsl:text>\langle </xsl:text>
	<xsl:for-each select="*[position()&gt;1]">
		<xsl:apply-templates select="."/>
		<xsl:if test="position() !=last()"><xsl:text>, </xsl:text></xsl:if>
	</xsl:for-each>
	<xsl:text>\rangle </xsl:text>
</xsl:template>

<!-- 4.4.9.2 sdef -->
<xsl:template match="m:sdev"><xsl:text>\sigma </xsl:text></xsl:template>

<!-- 4.4.9.3 variance -->
<xsl:template match="m:apply[*[1][self::m:variance]]">
	<xsl:text>\sigma(</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>)^2</xsl:text>
</xsl:template>

<!-- 4.4.9.5 moment -->
<xsl:template match="m:apply[*[1][self::m:moment]]">
	<xsl:text>\langle </xsl:text>
	<xsl:apply-templates select="*[last()]"/>
	<xsl:text>^{</xsl:text>
	<xsl:apply-templates select="m:degree/node()"/>
	<xsl:text>}\rangle</xsl:text>
	<xsl:if test="m:momentabout">
		<xsl:text>_{</xsl:text>
		<xsl:apply-templates select="m:momentabout/node()"/>
		<xsl:text>}</xsl:text>
	</xsl:if>
	<xsl:text> </xsl:text>
</xsl:template>

<!-- 4.4.10.1 vector  -->
<xsl:template match="m:vector">
	<xsl:text>\left(\begin{array}{c}</xsl:text>
	<xsl:for-each select="*">
		<xsl:apply-templates select="."/>
		<xsl:if test="position()!=last()"><xsl:text>\\ </xsl:text></xsl:if>
	</xsl:for-each>
	<xsl:text>\end{array}\right)</xsl:text>
</xsl:template>

<!-- 4.4.10.2 matrix  -->
<xsl:template match="m:matrix">
	<xsl:text>\begin{pmatrix}</xsl:text>
	<xsl:apply-templates/>
	<xsl:text>\end{pmatrix}</xsl:text>
</xsl:template>

<!-- 4.4.10.3 matrixrow  -->
<xsl:template match="m:matrixrow">
	<xsl:for-each select="*">
		<xsl:apply-templates select="."/>
		<xsl:if test="position()!=last()"><xsl:text> &amp; </xsl:text></xsl:if>
	</xsl:for-each>
	<xsl:if test="position()!=last()"><xsl:text>\\ </xsl:text></xsl:if>
</xsl:template>

<!-- 4.4.10.4 determinant  -->
<xsl:template match="m:apply[*[1][self::m:determinant]]">
	<xsl:text>\det </xsl:text>
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="m:apply[*[1][self::m:determinant]][*[2][self::m:matrix]]" priority="2">
	<xsl:text>\begin{vmatrix}</xsl:text>
	<xsl:apply-templates select="m:matrix/*"/>
	<xsl:text>\end{vmatrix}</xsl:text>
</xsl:template>

<!-- 4.4.10.5 transpose -->
<xsl:template match="m:apply[*[1][self::m:transpose]]">
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
	<xsl:text>^T</xsl:text>
</xsl:template>

<!-- 4.4.10.5 selector -->
<xsl:template match="m:apply[*[1][self::m:selector]]">
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="7"/>
	</xsl:apply-templates>
	<xsl:text>_{</xsl:text>
	<xsl:for-each select="*[position()&gt;2]">
		<xsl:apply-templates select="."/>
		<xsl:if test="position() !=last()"><xsl:text>, </xsl:text></xsl:if>
	</xsl:for-each>
	<xsl:text>}</xsl:text>
</xsl:template>

<!-- 4.4.10.7 scalarproduct 4.4.10.8 outerproduct -->
<xsl:template match="m:apply[*[1][self::m:scalarproduct or self::m:outerproduct]]">
	<xsl:param name="p" select="0"/>
	<xsl:call-template name="infix">
		<xsl:with-param name="this-p" select="2"/>
		<xsl:with-param name="p" select="$p"/>
		<xsl:with-param name="mo">\dot </xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- 4.4.11.2 semantics -->
<xsl:template match="m:semantics"><xsl:apply-templates select="*[1]"/></xsl:template>

<xsl:template match="m:semantics[m:annotation/@encoding='TeX']">
	<xsl:apply-templates select="m:annotation[@encoding='TeX']/node()"/>
</xsl:template>

<!-- 4.4.12.1 integers -->
<xsl:template match="m:integers"><xsl:text>\mathbb{Z}</xsl:text></xsl:template>

<!-- 4.4.12.2 reals -->
<xsl:template match="m:reals"><xsl:text>\mathbb{R}</xsl:text></xsl:template>

<!-- 4.4.12.3 rationals -->
<xsl:template match="m:rationals"><xsl:text>\mathbb{Q}</xsl:text></xsl:template>

<!-- 4.4.12.4 naturalnumbers -->
<xsl:template match="m:naturalnumbers"><xsl:text>\mathbb{N}</xsl:text></xsl:template>

<!-- 4.4.12.5 complexes -->
<xsl:template match="m:complexes"><xsl:text>\mathbb{C}</xsl:text></xsl:template>

<!-- 4.4.12.6 primes -->
<xsl:template match="m:primes"><xsl:text>\mathbb{P}</xsl:text></xsl:template>
	
<!-- 4.4.12.7 exponentiale -->
<xsl:template match="m:exponentiale"><xsl:text>e</xsl:text></xsl:template>

<!-- 4.4.12.8 imaginaryi -->
<xsl:template match="m:imaginaryi"><xsl:text>i</xsl:text></xsl:template>

<!-- 4.4.12.9 notanumber -->
<xsl:template match="m:notanumber"><xsl:text>NaN</xsl:text></xsl:template>

<!-- 4.4.12.10 true -->
<xsl:template match="m:true"><xsl:text>\mbox{true}</xsl:text></xsl:template>

<!-- 4.4.12.11 false -->
<xsl:template match="m:false"><xsl:text>\mbox{false}</xsl:text></xsl:template>

<!-- 4.4.12.12 emptyset -->
<xsl:template match="m:emptyset"><xsl:text>\emptyset </xsl:text></xsl:template>

<!-- 4.4.12.13 pi -->
<xsl:template match="m:pi"><xsl:text>\pi </xsl:text></xsl:template>

<!-- 4.4.12.14 eulergamma -->
<xsl:template match="m:eulergamma"><xsl:text>\gamma </xsl:text></xsl:template>

<!-- 4.4.12.15 infinity -->
<xsl:template match="m:infinity"><xsl:text>\infty </xsl:text></xsl:template>

<!-- ****************************** -->
<xsl:template name="infix" >
  <xsl:param name="mo"/>
  <xsl:param name="p" select="0"/>
  <xsl:param name="this-p" select="0"/>
  <xsl:if test="$this-p &lt; $p"><xsl:text>(</xsl:text></xsl:if>
  <xsl:for-each select="*[position()&gt;1]">
		<xsl:if test="position() &gt; 1">
			<xsl:copy-of select="$mo"/>
		</xsl:if>   
		<xsl:apply-templates select=".">
			<xsl:with-param name="p" select="$this-p"/>
		</xsl:apply-templates>
	</xsl:for-each>
  <xsl:if test="$this-p &lt; $p"><xsl:text>)</xsl:text></xsl:if>
</xsl:template>

<xsl:template name="binary" >
  <xsl:param name="mo"/>
  <xsl:param name="p" select="0"/>
  <xsl:param name="this-p" select="0"/>
  <xsl:if test="$this-p &lt; $p"><xsl:text>(</xsl:text></xsl:if>
	<xsl:apply-templates select="*[2]">
		<xsl:with-param name="p" select="$this-p"/>
	</xsl:apply-templates>
	<xsl:value-of select="$mo"/>
	<xsl:apply-templates select="*[3]">
    	<xsl:with-param name="p" select="$this-p"/>
	</xsl:apply-templates>
	<xsl:if test="$this-p &lt; $p"><xsl:text>)</xsl:text></xsl:if>
</xsl:template>

</xsl:stylesheet>