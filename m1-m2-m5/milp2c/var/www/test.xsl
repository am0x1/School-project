<?xml version="1.0"?>
 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 
   <xsl:template match="/">
 
     <html>
       <head><link rel="stylesheet" type="text/css" href="http://localhost:80/test.css" /> </head>
       <body>
 	<h1>Poems</h1>
 
 	<table border="1">
 
 	  <tr>
 	    <th>poemID</th> <th>poemtext</th> <th>email</th>
 	  </tr>
 
 	  <xsl:for-each select="poems/poem">
 	    <xsl:sort select="felt[@navn='tittel']"/>
 
 	    <tr>
 		<td><xsl:value-of select="poemID"/> </td>
 		<td><xsl:value-of select="poemtext"/> </td>
 		<td><xsl:value-of select="email"/> </td>
 	    </tr>
 
 	  </xsl:for-each>
 
 	</table>
       </body>
     </html>
   </xsl:template>
 
</xsl:stylesheet>
