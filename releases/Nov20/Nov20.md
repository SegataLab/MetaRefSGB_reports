# Report for the Nov20 release
## Releases overview


Release | Total MAGs | Total Reference Genomes | New MAGs | New Reference Genomes | Total kSGBs | Total uSGBs | New kSGBs | New uSGBs | Unknown to known
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
[Jan19](../Jan19/Jan19.md)	| 160267	| 75446	| 160267	| 75446	| 9641	| 6690	| 9641	| 6690	| 0
[May19](../May19/May19.md)	| 163252	| 75446	| 2985	| 0	| 9641	| 7699	| 0	| 1009	| 0
[Jun19](../Jun19/Jun19.md)	| 165219	| 100133	| 1967	| 24687	| 11355	| 8478	| 1555	| 938	| 159
[Jul19](../Jul19/Jul19.md)	| 166454	| 100133	| 1235	| 0	| 11355	| 9537	| 0	| 1059	| 0
[Aug19](../Aug19/Aug19.md)	| 170038	| 100133	| 3584	| 0	| 11355	| 9683	| 0	| 146	| 0
[Sep19](../Sep19/Sep19.md)	| 170148	| 138564	| 110	| 38431	| 16529	| 9420	| 4909	| 2	| 265
[Oct19](../Oct19/Oct19.md)	| 178808	| 138564	| 8660	| 0	| 16529	| 12720	| 0	| 3300	| 0
[Nov19](../Nov19/Nov19.md)	| 214092	| 138588	| 35284	| 24	| 16533	| 16822	| 4	| 4102	| 0
[Dec19](../Dec19/Dec19.md)	| 343550	| 141702	| 129458	| 3114	| 18350	| 28209	| 1768	| 11436	| 49
[Jan20](../Jan20/Jan20.md)	| 427414	| 138651	| 83864	| 0	| 17190	| 30672	| 4	| 6995	| 17
[Jul20](../Jul20/Jul20.md)	| 436838	| 139472	| 9424	| 821	| 17527	| 33793	| 84	| 3374	| 253
[Sep20](../Sep20/Sep20.md)	| 447463	| 139471	| 10625	| 0	| 17527	| 34276	| 0	| 483	| 0
[Nov20](../Nov20/Nov20.md)	| 499902	| 139478	| 52439	| 7	| 17512	| 37458	| 3	| 3526	| 19

## Nov20 release overview


Level | Bacteria | Archaea | Eukaryota | Total
------------ | ------------- | ------------- | ------------- | -------------
Other	| 25494	| 657	| 0	| 26151	| 0.0
Species	| 16985	| 527	| 0	| 17512	| 0.0
Family	| 5745	| 328	| 0	| 6073	| 0.0
Genus	| 5137	| 97	| 0	| 5234	| 0.0


Histogram showing the number of `kSGBs`, `uSGBs`, `reconstructed` and `reference genomes` included in Nov20

![Number of kSGBs, uSGBs, reconstructed and reference genomes](pictures/first_fig1.jpg)


Histogram showing the number of **NEW** `kSGBs`, `uSGBs`, `reconstructed` and `reference genomes` included in Nov20

![Number of NEW kSGBs, uSGBs, reconstructed and reference genomes](pictures/first_fig2.jpg)


## Distribution of the kSGBs by number of genomes in the database
Histograms showing the distribution density of kSGBs by the number of genomes in the database. In particular, the number of kSGBs that have respectively from 0 to 10 reconstructed and reference genomes are shown. In the 12th column there is a grouping of all the others with more than 10.

![The number of genomes for each kSGB](pictures/first_fig3.jpg)


## Distribution of the uSGBs by number of genomes in the database
Histograms showing the distribution density of uSGBs by the number of genomes in the database. In particular, the number of uSGBs that have respectively from 0 to 10 reconstructed and reference genomes are shown. In the 12th column there is a grouping of all the others with more than 10.

![The number of genomes for each uSGB](pictures/first_fig4.jpg)


## Number of SGBs by the level of assigned taxonomy
Histogram showing the number of SGBs by their lower level of known taxonomy.

![Number of SGBs by the level of assigned taxonomy](pictures/first_fig5.jpg)


<table><tr><th colspan = '2' style = 'text-align: center'>Phylum</th><th colspan = '2' style = 'text-align: center'>Family</th><th colspan = '2' style = 'text-align: center'>Genus</th><th colspan = '2' style = 'text-align: center'>Species</th></tr><tr><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th></tr><tr><td>Firmicutes</td><td>8435</td><td>Prochloraceae</td><td>756</td><td>Prochlorococcus</td><td>752</td><td>Ruminococcaceae bacterium</td><td>179</td></tr><tr><td>Proteobacteria</td><td>7684</td><td>Ruminococcaceae</td><td>709</td><td>Pelagibacteraceae unclassified</td><td>706</td><td>Rhizobiales bacterium</td><td>91</td></tr><tr><td>Bacteroidetes</td><td>3746</td><td>Prevotellaceae</td><td>346</td><td>Collinsella</td><td>325</td><td>Buchnera aphidicola</td><td>49</td></tr><tr><td>Actinobacteria</td><td>2683</td><td>Lachnospiraceae</td><td>286</td><td>Candidatus Pelagibacter</td><td>235</td><td>Pseudomonas fluorescens</td><td>46</td></tr><tr><td>Euryarchaeota</td><td>443</td><td>Pelagibacteraceae</td><td>147</td><td>Ruminococcaceae unclassified</td><td>124</td><td>Streptococcus mitis</td><td>35</td></tr><tr><td>Candidatus Saccharibacteria</td><td>334</td><td>Candidatus Gastranaerophilales unclassified</td><td>134</td><td>Streptococcus</td><td>117</td><td>Fibrobacter succinogenes</td><td>29</td></tr><tr><td>Tenericutes</td><td>330</td><td>Flavobacteriaceae</td><td>131</td><td>Microbacterium</td><td>105</td><td>Pseudomonas viridiflava</td><td>29</td></tr><tr><td>Spirochaetes</td><td>281</td><td>Bacteroidales unclassified</td><td>129</td><td>Alphaproteobacteria unclassified</td><td>87</td><td>Ruminococcus flavefaciens</td><td>28</td></tr><tr><td>Fusobacteria</td><td>279</td><td>Clostridiales unclassified</td><td>122</td><td>Campylobacter</td><td>82</td><td>Rhodobacteraceae bacterium</td><td>26</td></tr><tr><td>Chloroflexi</td><td>197</td><td>Clostridiaceae</td><td>113</td><td>Prevotella</td><td>66</td><td>Stenotrophomonas maltophilia</td><td>26</td></tr><tr style = 'font-weight: bold'><td>Others</td><td>1739</td><td>Others</td><td>3200</td><td>Others</td><td>2635</td><td>Others</td><td>16973</td></tr></table>

## Number of uSGBs with, at least 5 MAGs, by the level of assigned taxonomy
Histogram showing the number of uSGBs, with at least 5 MAGs in the database, by their lower level of known taxonomy.

![Number of uSGBs with, at least, 5 MAGs by the level of assigned taxonomy](pictures/first_fig6.jpg)


## Taxonomies assigned at the Phylum level for uSGBs with, at least, 5 MAGs
Percentage of uSGBs with, at least, 5 MAGs assigned to different phylum.

![Percentage of taxonomies assigned at the Phylum level of uSGBs that have at least 5 MAGs](pictures/first_fig7.jpg)


## Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs
Percentage of uSGBs with, at least, 5 MAGs assigned to different families. The top 10 assigned families are shown in the histogram in the right.

![Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs](pictures/first_fig8.jpg)


## Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs
Percentage of uSGBs with, at least, 5 MAGs assigned to different genus. The top 10 assigned genus are shown in the histogram in the right.

![Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs](pictures/first_fig9.jpg)


## Number of alternative taxonomies for the kSGBs
Histogram representing the distribution of kSGBs by the number of alternative taxonomies. 

![Number of kSGBs by the number of the alternative taxonomies](pictures/first_fig10.jpg)


## Distribution of kSGBs by their proportion of reference genomes belonging to the assigned taxonomy
Histogram showing the distribution of kSGBs by the proportion of the reference genomes belonging to the assigned taxonomy.

![Distribution of kSGBs by their proportion of genomes belonging the assigned taxonomy](pictures/first_fig11.jpg)


## SGBs with 2 alternative taxonomies in a 50 / 50 proportion
Histogram reporting the SGBs with 2 alternative taxonomies in a 50 / 50 genomes proportion. We defined 3 groups: "Binary : Binary", "Binary : Non-Binary" and "Non-Binary : Non-Binary". Binary we mean that the taxonomy respects the criteria values set by the regular expression reported here " `(.*(C|c)andidat(e|us)_.*)|(.*_sp(_.*|$))|((.*_|^)(b|B)acterium(_.*|$))|(.*(eury|)archaeo(n_|te).*)|(.*(endo|)symbiont.*|.*genomosp_.* |.*unidentified.*|.*_bacteria_.*|.*_taxon_.*|.*_et_al_.*|.*_and_.*|.*(cyano|proteo|actino)bacterium_.*)` ", while Non-Binary mean the opposite.

### [Here](pages/df_first_fig12.md) you can see the list of SGBs.

![SGBs with 2 alternative taxonomies in a 50 / 50 proportion](pictures/first_fig12.jpg)

## Taxonomic differences in the alternative taxonomies for the SGBs with 2 alternative taxonomues in a 50 / 50 proporyion
Histogram showing, for the `Binary : Binary` group the number of SGBs by the higher taxonomic level that differs between the two alternative taxonomies.

### [Here](pages/df_first_fig13.md) you can see the list of SGBs.

![Number of SGBs by the higher taxonomic level that differs between the to alternative taxonomies. `Binary : Binary` group](pictures/first_fig13.jpg)


The same as the previous one applies to this but with `Binary : Non-Binary` (obiously also the complementary one).

### [Here](pages/df_first_fig14.md) you can see the list of SGBs.

![Number of SGBs by the higher taxonomic level that differs between the to alternative taxonomies. `Binary : Non-Binary` group](pictures/first_fig14.jpg)


The same as the previous one applies to this but with `Non-Binary : Non-Binary`.

### [Here](pages/df_first_fig15.md) you can see the list of SGBs.

![Number of SGBs by the higher taxonomic level that differs between the to alternative taxonomies. `Non-Binary : Non-Binary` group](pictures/first_fig15.jpg)


## Taxonomic families per FGB
This graph shows the number of families present in a single FGB. The first column shows the number of FGBs that have associated only one family, while the second shows thos that have that associated more than one.

![Taxonomic families per FGB](pictures/first_fig16.jpg)

### [Here](pages/df_first_fig16.md) the list of FGBs with their families

### [Here](pages/df_first_fig16_more1.md) the list of FGBs with more than one family

### [Here](pages/df_first_fig16_only1.md) the list of FGBs with only one familiy

## Taxonomic genera present in several FGBs
Histogram showing the number of genera appearing in one or more FGBs. In the first column there are the number of those that appear only in one FGB, while in the second those that appear in more than one.

![Taxonomic genera present in several FGBs](pictures/first_fig17.jpg)

### [Here](pages/df_first_fig17.md) the list of FGBs with their genus

### [Here](pages/df_first_fig17_more1.md) the list of FGBs with more than one genus

### [Here](pages/df_first_fig17_only1.md) the list of FGBs with only one genus

