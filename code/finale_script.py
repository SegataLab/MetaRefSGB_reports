# %%
# First conficurations

def progress_bar(progress: int = 0, total: int = 100, dim: int = 100, char: str = '#', custom_str: str = "") -> None:       #█
    percent = 100 * float(progress / float(total))
    alg_percent = dim * (progress / float(total))
    bar = char * int(alg_percent) + '-' * (dim - int(alg_percent))
    if custom_str == "":
        print(f"\r[{bar}] {percent:.4f}% - {progress}/{total}", end = "\r")
    else:
        print(f"\r[{bar}] {percent:.4f}% - {progress}/{total} - {custom_str}", end = "\r")

def apply_penality_tax(taxonomy: str, level: int, reg_exp_list: list) -> int:       # Calcolo la penalità nella stringa della tassonomia
    penality = 0                                                    
    for reg_exp in reg_exp_list:
        if reg_exp.match(taxonomy.split(":")[0].split("|")[level]):
            penality += 1
    return penality

def apply_penality_str(target: str, reg_exp_list: list) -> int:                     # Calcolo la penalità della stringa
    penality = 0                                                    
    for reg_exp in reg_exp_list:
        if reg_exp.match(target):
            penality += 1
    return penality

from datetime import datetime
import threading as th
import sys
import os
import bz2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import shutil
import re
import myClass as mc

start = datetime.now()
steps = 0
max_timer = 26
script_delete = False

FILES = "files/"
PAGES = "pages/"
PICTURES = "pictures/"
RELEASES = "../releases/"

PAST_FILE_const = "NaN00"
FILE_const = "NaN01"              # Nome della release
FILES_const = RELEASES + FILE_const[:5] + "/" + FILES
PAGES_const = RELEASES + FILE_const[:5] + "/" + PAGES
PICTURES_const = RELEASES + FILE_const[:5] + "/" + PICTURES

def thread():
    print("\033[0;93m", end = "") # Yellow
    while(steps < max_timer):
        progress_bar(steps, max_timer, custom_str = f"{int((datetime.now() - start).total_seconds())} sec - {FILE_const[:5]}       ")

    print("\033[0;92m", end = "") # Green
    progress_bar(steps, max_timer, custom_str = f"{int((datetime.now() - start).total_seconds())} sec       ")
    print("\033[0;37m", end = "") # White
    print("\n")
    
argv = list(sys.argv)
if len(argv) > 1:
    if argv[1] == "True":
        tr = th.Thread(target = thread)
        tr.start()

MAPPING_MONTH = {
    "NaN" : 0, "Jan" : 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12
}

my_colors = {
    'violet'        : (0.3450764705882353 , 0.0                , 0.6235411764705882 ),  # Num of MAGs
    'purple'        : (0.5097941176470588 , 0.0                , 0.5764588235294118 ),  # Kingdom
    'dark_magenta'  : (0.5752941176470587 , 0.19588235294117648, 0.5205882352941177 ),  # kSGB
    'magenta'       : (0.9098039215686274 , 0.09019607843137256, 1.0                ),  # Binary : Binary
    'lilla'         : (0.5450980392156862 , 0.4549019607843138 , 1.0                ),  # Binary : Non-Binary
    'blue'          : (0.0                , 0.1464156862745098 , 0.8667             ),  # uSGB
    'light_blue'    : (0.0                , 0.46931372549019607, 0.8667             ),  # Phylum
    'cyan'          : (0.0                , 0.6444666666666666 , 0.7333666666666667 ),  # Class
    'sky'           : (0.09019607843137255, 0.9098039215686274 , 1.0                ),  # Non-Binary : Non-Binary
    'green'         : (0.0                , 0.7385313725490196 , 0.0                ),  # Order
    'lime'          : (0.6901647058823529 , 1.0                , 0.0                ),  # Family
    'light_orange'  : (1.0                , 0.7882352941176471 , 0.0                ),  # Num of Ref Genomes
    'orange'        : (1.0                , 0.3176470588235294 , 0.0                ),  # Genus
    'red'           : (0.8431588235294118 , 0.0                , 0.0                ),  # Species
    'pink_flesh'    : (1.0                , 0.6705882352941177 , 0.3411764705882354 )   # Num alt tax
}

# Lista delle release da filtrare
f = os.listdir('/shares/CIBIO-Storage/CM/scratch/databases/MetaRefSGB/releases')
files = list()
for x in sorted(f):
    res = ""
    if x[:3] == "Jan":
        res = "01"
    elif x[:3] == "Feb":
        res = "02"
    elif x[:3] == "Mar":
        res = "03"
    elif x[:3] == "Apr":
        res = "04"
    elif x[:3] == "May":
        res = "05"
    elif x[:3] == "Jun":
        res = "06"
    elif x[:3] == "Jul":
        res = "07"
    elif x[:3] == "Aug":
        res = "08"
    elif x[:3] == "Sep":
        res = "09"
    elif x[:3] == "Oct":
        res = "10"
    elif x[:3] == "Nov":
        res = "11"
    elif x[:3] == "Dec":
        res = "12"
    else:
        continue
        
    if len(x) == 11:        # Caso in cui la release sia aggiornata
        files[len(files) - 1] = ((x[:11], res, x[3] + x[4]))
    else:
        files.append((x[:5], res, x[3] + x[4]))   

lf = list()
for p in sorted(files, key = lambda x : (x[2], x[1])):
    if p[0] not in lf:
        lf.append(p[0])
files = lf                  # Lista completa delle release

max_timer = (max_timer - 1) * len(files)
steps += 1

tab = pd.DataFrame(
    columns = [
        "Release",
        "Total MAGs",
        "Total Reference Genomes",
        "New MAGs",
        "New Reference Genomes",
        "Total kSGBs",
        "Total uSGBs",
        "New kSGBs",
        "New uSGBs",
        "Unknown to Known"
    ]
)

# Controlla la presenza delle cartelle utili
if not os.path.exists(RELEASES):
    os.mkdir(RELEASES)

sgb_new = pd.DataFrame(columns = ["Label", "ID", "Number of reconstructed genomes", "Number of reference genomes", "List of reconstructed genomes", "List of reference genomes", "SGB centroid", "Unknown", "Level of assigned taxonomy", "Assigned taxonomy", "Assigned taxonomic ID", "Number of Alternative taxonomies", "List of alternative taxonomies", "List of alternative taxonomic IDs"])
for index_file in range(len(files)):
    FILE_const = files[index_file]
    FILES_const = RELEASES + FILE_const[:5] + "/" + FILES
    PAGES_const = RELEASES + FILE_const[:5] + "/" + PAGES
    PICTURES_const = RELEASES + FILE_const[:5] + "/" + PICTURES

    # Controlla la presenza delle cartelle utili
    if not os.path.exists(RELEASES + FILE_const[:5]):
        os.mkdir(RELEASES + FILE_const[:5])
    if not os.path.exists(FILES_const[:-1]):
        os.mkdir(FILES_const[:-1])
    if not os.path.exists(PAGES_const[:-1]):
        os.mkdir(PAGES_const[:-1])
    if not os.path.exists(PICTURES_const[:-1]):
        os.mkdir(PICTURES_const[:-1])

    # Conto le righe da saltare
    with bz2.open("/shares/CIBIO-Storage/CM/scratch/databases/MetaRefSGB/releases/" + files[index_file] + "/SGB." + files[index_file] + ".txt.bz2", 'rt') as read_file:
        for count, x in enumerate(read_file):
            if x[:7] == "# Label":
                break
    read_file.close()

    # Punta alla vecchia release
    sgb_old = sgb_new

    # Punta alla nuova release
    with bz2.open("/shares/CIBIO-Storage/CM/scratch/databases/MetaRefSGB/releases/" + files[index_file] + "/SGB." + files[index_file] + ".txt.bz2", 'rt') as read_file:
        df_new = pd.read_csv(read_file, sep = "\t", skiprows = count)
    df_new = df_new.rename(columns = {"# Label" : "Label"})
    sgb_new = df_new[df_new["Label"] == "SGB"]
    
    # DataFrame per la verifica dei casi nuovi
    test = sgb_new[sgb_new["ID"].isin(set(sgb_new["ID"]) - set(sgb_old["ID"]))]

    # Valori per ogni riga
    release = files[index_file][:5]
    total_mag = sgb_new["Number of reconstructed genomes"].sum()
    total_ref = sgb_new["Number of reference genomes"].sum()
    new_mag = sgb_new["Number of reconstructed genomes"].sum() - sgb_old["Number of reconstructed genomes"].sum()
    new_ref = sgb_new["Number of reference genomes"].sum() - sgb_old["Number of reference genomes"].sum()
    total_kSGB = len(sgb_new[sgb_new["Unknown"] == "kSGB"])
    total_uSGB = len(sgb_new[sgb_new["Unknown"] == "uSGB"])
    new_kSGB = len(test[test["Unknown"] == "kSGB"])
    new_uSGB = len(test[test["Unknown"] == "uSGB"])

    # Upgrade from uSGB to kSGB
    sgb_old3 = pd.DataFrame(
        data = sgb_old[["ID", "Unknown"]]
    )
    sgb_new3 = pd.DataFrame(
        data = sgb_new[["ID", "Unknown"]]
    )
    sgb_comparison_merged = pd.merge(sgb_old3, sgb_new3, on = "ID", suffixes = ["_old", "_new"])

    upgrade = 0
    for i in sgb_comparison_merged.index:
        if (sgb_comparison_merged.loc[i]["Unknown_old"] == "uSGB") & (sgb_comparison_merged.loc[i]["Unknown_new"] == "kSGB"):
            upgrade += 1
    u_to_k = upgrade

    # Aggiunta della riga alla tabella
    tab = pd.concat([
        tab,
        pd.DataFrame(
            data = {
                "Release"                   : [release],
                "Total MAGs"                : [max(0, total_mag)],
                "Total Reference Genomes"   : [max(0, total_ref)],
                "New MAGs"                  : [max(0, new_mag)],
                "New Reference Genomes"     : [max(0, new_ref)],
                "Total kSGBs"               : [max(0, total_kSGB)],
                "Total uSGBs"               : [max(0, total_uSGB)],
                "New kSGBs"                 : [max(0, new_kSGB)],
                "New uSGBs"                 : [max(0, new_uSGB)],
                "Unknown to Known"          : [max(0, u_to_k)]
            }
        )
    ], ignore_index = True)
    
    steps += 1

    # Inizio statistiche file
    tab_sgb_lev = pd.DataFrame(columns = ["Bacteria", "Archaea", "Eukaryota", "Total"])
    for i_tax in sgb_new["Level of assigned taxonomy"].value_counts().index:
        tab_sgb_lev = pd.concat([
            tab_sgb_lev,
            pd.DataFrame(
                data = {
                    "Bacteria"  : [0],
                    "Archaea"   : [0],
                    "Eukaryota" : [0],
                    "Total"     : [0],
                    "Others"    : [0]
                },
                index = [i_tax]
            )
        ])

    for i_tax in sgb_new.index:
        pos_tax = "pppp"
        if sgb_new.loc[i_tax]["Assigned taxonomy"].split("|")[0] == "k__Bacteria":
            pos_tax = "Bacteria"
        elif sgb_new.loc[i_tax]["Assigned taxonomy"].split("|")[0] == "k__Archaea":
            pos_tax = "Archaea"
        elif sgb_new.loc[i_tax]["Assigned taxonomy"].split("|")[0] == "k__Eukaryota":
            pos_tax = "Eukaryota"
        
        tab_sgb_lev[pos_tax].at[sgb_new.loc[i_tax]["Level of assigned taxonomy"]] += 1

    for i_tax in tab_sgb_lev.index:
        tab_sgb_lev["Total"].at[i_tax] = tab_sgb_lev.loc[i_tax]["Bacteria"] + tab_sgb_lev.loc[i_tax]["Archaea"] + tab_sgb_lev.loc[i_tax]["Eukaryota"]
    
    plt.tight_layout()

    # %%
    plt.close("all")
    first_fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,7))

    first_fig1.set_facecolor("w")
    first_fig1.suptitle("Number of kSGBs, uSGBs, reconstructed and reference genomes", color = ('brown'), fontsize = 16, fontweight = "bold")
    plot = sb.barplot(
        data = pd.DataFrame(
            {
                "lab" : ["kSGB", "uSGB"],
                "val" : [total_kSGB, total_uSGB]
            }
        ),
        x = "lab",
        y = "val",
        ax = ax1,
        palette = [my_colors["blue"], my_colors["dark_magenta"]]
    )
    plot.set(xlabel = None)
    plot.set(ylabel = None)

    plot.text(0, 0.5 * plot.patches[0].get_height(), str(len(sgb_new[sgb_new["Unknown"] == "kSGB"])), horizontalalignment = 'center', ha = "center", va = "center", color = "white")
    plot.text(1, 0.5 * plot.patches[1].get_height(), str(len(sgb_new[sgb_new["Unknown"] == "uSGB"])), horizontalalignment = 'center', ha = "center", va = "center", color = "white")

    plot = sb.barplot(
        data = pd.DataFrame(
            {
                "lab" : ["Reconstructed genomes", "Reference genomes"],
                "val" : [total_mag, total_ref]
            }
        ),
        x = "lab",
        y = "val",
        ax = ax2,
        palette = [my_colors["violet"], my_colors["light_orange"]]
    )
    plot.set(xlabel = None)
    plot.set(ylabel = None)

    plot.text(0, 0.5 * plot.patches[0].get_height(), str(sgb_new["Number of reconstructed genomes"].sum()), horizontalalignment = 'center', ha = "center", va = "center", color = "white")
    plot.text(1, 0.5 * plot.patches[1].get_height(), str(sgb_new["Number of reference genomes"].sum()), horizontalalignment = 'center', ha = "center", va = "center", color = "white")

    steps += 1

    plt.tight_layout()

    # %%
    test = sgb_new[sgb_new["ID"].isin(set(sgb_new["ID"]) - set(sgb_old["ID"]))]

    plt.close("all")
    first_fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,7))

    first_fig2.set_facecolor("w")
    first_fig2.suptitle("Number of NEW kSGBs, uSGBs, reconstructed and reference genomes", color = ('brown'), fontsize = 16, fontweight = "bold")
    plot = sb.barplot(
        data = pd.DataFrame(
            {
                "lab" : ["kSGB", "uSGB"],
                "val" : [new_kSGB, new_uSGB]
            }
        ),
        x = "lab",
        y = "val",
        ax = ax1,
        palette = [my_colors["blue"], my_colors["dark_magenta"]]
    )
    plot.set(xlabel = None)
    plot.set(ylabel = None)

    plot.text(0, 0.5 * plot.patches[0].get_height(), str(new_kSGB), horizontalalignment = 'center', ha = "center", va = "center", color = "white")
    plot.text(1, 0.5 * plot.patches[1].get_height(), str(new_uSGB), horizontalalignment = 'center', ha = "center", va = "center", color = "white")

    plot = sb.barplot(
        data = pd.DataFrame(
            {
                "lab" : ["Reconstructed genomes", "Reference genomes"],
                "val" : [new_mag, new_ref]
            }
        ),
        x = "lab",
        y = "val",
        ax = ax2,
        palette = [my_colors["violet"], my_colors["light_orange"]]
    )
    plot.set(xlabel = None)
    plot.set(ylabel = None)

    plot.text(0, 0.5 * plot.patches[0].get_height(), str(new_mag), horizontalalignment = 'center', ha = "center", va = "center", color = "white")
    plot.text(1, 0.5 * plot.patches[1].get_height(), str(new_ref), horizontalalignment = 'center', ha = "center", va = "center", color = "white")

    steps += 1

    plt.tight_layout()

    # %%
    # The number of genomics for each kSGB. It can be also divided by reconstructed and reference genomes.

    test = sgb_new[sgb_new["Unknown"] == "kSGB"]
    test = test[["Number of reconstructed genomes", "Number of reference genomes"]]

    more100 = test[test["Number of reconstructed genomes"] > 10]
    if 12 not in more100["Number of reconstructed genomes"]:
        for i in more100.index:
            test["Number of reconstructed genomes"].at[i] = 12
    else:
        print("error")

    more100 = test[test["Number of reference genomes"] > 10]
    if 12 not in more100["Number of reference genomes"]:
        for i in more100.index:
            test["Number of reference genomes"].at[i] = 12
    else:
        print("error")

    # Plot "SGB1.jpg"
    plt.close("all")
    first_fig3, (ax1, ax2) = plt.subplots(2, 1, sharex = False, figsize = (12, 7))

    first_fig3.set_facecolor("w")
    first_fig3.suptitle("The number of genomes for each kSGB", color = ('brown'), fontsize = 16, fontweight = "bold")

    # first
    plt.setp(ax1, xticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xticklabels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "", "> 10"])
    plot = sb.histplot(data = test, x = "Number of reconstructed genomes", stat = "density", discrete = True, ax = ax1, color = my_colors["violet"])
    count = test["Number of reconstructed genomes"].value_counts()
    for i in range(11):
        if plot.patches[i].get_height() > 0.5:
            c = "white"
        else:
            c = "black"
        
        if i not in count.index:
            plot.text(i, 0.5, str(0), horizontalalignment = 'center', color = c)
        else:
            plot.text(i, 0.5, str(count[i]), horizontalalignment = 'center', color = c)
    plot.text(12, 0.5, str(count[12]), horizontalalignment = 'center', color = c)

    # second
    plt.setp(ax2, xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xticklabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "", "> 10"])
    plot = sb.histplot(data = test, x = "Number of reference genomes", stat = "density", discrete = True, ax = ax2, color = my_colors["light_orange"])
    count = test["Number of reference genomes"].value_counts()
    for i in range(1, 11):
        if plot.patches[i].get_height() > 0.5:
            c = "white"
        else:
            c = "black"
        
        if i not in count.index:
            plot.text(i, 0.5, str(0), horizontalalignment = 'center', color = c)
        else:
            plot.text(i, 0.5, str(count[i]), horizontalalignment = 'center', color = c)
    plot.text(12, 0.5, str(count[12]), horizontalalignment = 'center', color = c)

    steps += 1

    plt.tight_layout()

    # %%
    # The number of genomics for each uSGB. It can be also divided by reconstructed and reference genomes.

    test = sgb_new[sgb_new["Unknown"] == "uSGB"]
    test = test[["Number of reconstructed genomes", "Number of reference genomes"]]

    more100 = test[test["Number of reconstructed genomes"] > 10]
    if 12 not in more100["Number of reconstructed genomes"]:
        for i in more100.index:
            test["Number of reconstructed genomes"].at[i] = 12
    else:
        print("error")

    # Plot
    plt.close("all")
    first_fig4, ax1 = plt.subplots(figsize = (12,3.5))

    first_fig4.set_facecolor("w")
    first_fig4.suptitle("The number of genomes for each uSGB", color = ('brown'), fontsize = 16, fontweight = "bold")

    plt.setp(ax1, xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xticklabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "", "> 10"])
    plot = sb.histplot(data = test, x = "Number of reconstructed genomes", stat = "density", discrete = True, ax = ax1, color = my_colors["violet"])
    count = test["Number of reconstructed genomes"].value_counts()
    for i in range(1, 11):
        if plot.patches[i].get_height() > 0.25:
            c = "white"
        else:
            c = "black"
        
        if i not in count.index:
            plot.text(i, 0.25, str(0), horizontalalignment = 'center', color = c)
        else:
            plot.text(i, 0.25, str(count[i]), horizontalalignment = 'center', color = c)
    plot.text(12, 0.25, str(count[12]), horizontalalignment = 'center', color = c)

    steps += 1

    plt.tight_layout()

    # %%
    # The number of SGB for each level of assigned taxonomy ("Level of assigned taxonomy" column).
    plt.close("all")
    first_fig5, ax1 = plt.subplots(figsize=(12,7))

    first_fig5.set_facecolor("w")
    first_fig5.suptitle("Number of SGBs by the level of assigned taxonomy", color = ('brown'), fontsize = 16, fontweight = "bold")
    
    tab_first_fig_5 = pd.DataFrame({
        "lab" : ["Other", "Family", "Genus", "Species"],
        "val" : [
            len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Other"]),
            len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Family"]),
            len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Genus"]),
            len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Species"])
        ]
    })

    plot = sb.barplot(
        data = tab_first_fig_5,
        x = "lab",
        y = "val",
        ax = ax1,
        palette = [my_colors["green"], my_colors["lime"], my_colors["orange"], my_colors["red"]]
    )
    plot.set(xlabel = "Level of assigned taxonomy")
    plot.set(ylabel = "Number of SGBs")

    plot.text(0, plot.patches[0].get_height() / 2., str(len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Other"])), horizontalalignment = 'center', ha = "center", va = "center", color = "black")
    plot.text(1, plot.patches[1].get_height() / 2., str(len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Family"])), horizontalalignment = 'center', ha = "center", va = "center", color = "black")
    plot.text(2, plot.patches[2].get_height() / 2., str(len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Genus"])), horizontalalignment = 'center', ha = "center", va = "center", color = "black")
    plot.text(3, plot.patches[3].get_height() / 2., str(len(sgb_new[sgb_new["Level of assigned taxonomy"] == "Species"])), horizontalalignment = 'center', ha = "center", va = "center", color = "white")

    steps += 1

    plt.tight_layout()

    # %%

    other = mc.Tree()
    family = mc.Tree()
    genus = mc.Tree()
    species = mc.Tree()

    for i in sgb_new.index:
        l = sgb_new.loc[i]["Assigned taxonomy"].split(",")[0].split(":")[0].split("|")
        if sgb_new.loc[i]["Level of assigned taxonomy"] == "Other":
            other.add_child(path = l, init = True)
        elif sgb_new.loc[i]["Level of assigned taxonomy"] == "Family":
            family.add_child(path = l, init = True)
        elif sgb_new.loc[i]["Level of assigned taxonomy"] == "Genus":
            genus.add_child(path = l, init = True)
        elif sgb_new.loc[i]["Level of assigned taxonomy"] == "Species":
            species.add_child(path = l, init = True)

    other = other.get_level(1)
    family = family.get_level(4)
    genus = genus.get_level(5)
    species = species.get_level(6)

    pie_data_other = other.get_dict_of_counter()
    pie_data_family = family.get_dict_of_counter()
    pie_data_genus = genus.get_dict_of_counter()
    pie_data_species = species.get_dict_of_counter()

    # Phylum
    m = pd.Series(pie_data_other, pie_data_other.keys()).sort_values(ascending = False)
    l_other = {}
    c = 0
    last = -1
    l_other["Others"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l_other[i[3:]] = m[i]
            l_other["Others"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l_other["Others"] = sum(m) - l_other["Others"]
    temp_out = l_other.pop("Others")

    l_other = [(l_other[i], i.replace("_", " ")) for i in l_other.keys()]
    l_other.sort(key = lambda tup: tup[1], reverse = False)
    l_other.sort(key = lambda tup: tup[0], reverse = True)
    
    l_other.append((temp_out, "Others"))

    # Family
    m = pd.Series(pie_data_family, pie_data_family.keys()).sort_values(ascending = False)
    l_family = {}
    c = 0
    last = -1
    l_family["Others"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l_family[i[3:]] = m[i]
            l_family["Others"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l_family["Others"] = sum(m) - l_family["Others"]
    temp_out = l_family.pop("Others")
    
    l_family = [(l_family[i], i.replace("_", " ")) for i in l_family.keys()]
    l_family.sort(key = lambda tup: tup[1], reverse = False)
    l_family.sort(key = lambda tup: tup[0], reverse = True)
    
    l_family.append((temp_out, "Others"))

    # Genus
    m = pd.Series(pie_data_genus, pie_data_genus.keys()).sort_values(ascending = False)
    l_genus = {}
    c = 0
    last = -1
    l_genus["Others"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l_genus[i[3:]] = m[i]
            l_genus["Others"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l_genus["Others"] = sum(m) - l_genus["Others"]
    temp_out = l_genus.pop("Others")
    
    l_genus = [(l_genus[i], i.replace("_", " ")) for i in l_genus.keys()]
    l_genus.sort(key = lambda tup: tup[1], reverse = False)
    l_genus.sort(key = lambda tup: tup[0], reverse = True)

    l_genus.append((temp_out, "Others"))

    # Species
    m = pd.Series(pie_data_species, pie_data_species.keys()).sort_values(ascending = False)
    l_species = {}
    c = 0
    last = -1
    l_species["Others"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l_species[i[3:]] = m[i]
            l_species["Others"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l_species["Others"] = sum(m) - l_species["Others"]
    temp_out = l_species.pop("Others")
    
    l_species = [(l_species[i], i.replace("_", " ")) for i in l_species.keys()]
    l_species.sort(key = lambda tup: tup[1], reverse = False)
    l_species.sort(key = lambda tup: tup[0], reverse = True)

    l_species.append((temp_out, "Others"))

    # %%
    # For the uSGB that have more than 4 (min 5) reconstructed genomes:
    # The number of SGB per each level of assigned taxonomy ('Level of assigned taxonomy' column)

    test = sgb_new[sgb_new["Number of reconstructed genomes"] > 4]
    test = test[test["Unknown"] == "uSGB"]
    test = pd.DataFrame(
        data = {
        "Level of assigned taxonomy" : test["Level of assigned taxonomy"].value_counts().index,
        "Number for level"           : test["Level of assigned taxonomy"].value_counts()
        }
    )

    # Plot
    plt.close("all")
    first_fig6, ax1 = plt.subplots(figsize=(12,7))

    first_fig6.set_facecolor("w")
    first_fig6.suptitle("Number of uSGBs wit, at least, 5 MAGs by the level of assigned taxonomy", color = ('brown'), fontsize = 16, fontweight = "bold")
    plot = sb.barplot(data = test, x = "Level of assigned taxonomy", y = "Number for level", ax = ax1, palette = [my_colors["green"], my_colors["lime"], my_colors["orange"]])
    for i, x in enumerate(test.index):
        plot.text(i, plot.patches[i].get_height() / 2., str(test.loc[x]["Number for level"]), horizontalalignment = 'center', ha = "center", va = "center", color = "black")

    steps += 1

    plt.tight_layout()

    # %%
    # Inside each taxonomy level (genus, family or other) -> we want to plot (pie plot)
    # the percentage of the assigned taxonomy.

    test = sgb_new[sgb_new["Number of reconstructed genomes"] > 4]
    test = test[test["Unknown"] == "uSGB"]

    tree = mc.Tree()
    other = mc.Tree()
    family = mc.Tree()
    genus = mc.Tree()

    for i in test.index:
        l = test.loc[i]["Assigned taxonomy"].split(",")[0].split(":")[0].split("|")
        if test.loc[i]["Level of assigned taxonomy"] == "Other":
            other.add_child(path = l, init = True)
        elif test.loc[i]["Level of assigned taxonomy"] == "Family":
            family.add_child(path = l, init = True)
        elif test.loc[i]["Level of assigned taxonomy"] == "Genus":
            genus.add_child(path = l, init = True)
        
        tree.add_child(path = l, init = True)

    other = other.get_level(1)
    family = family.get_level(4)
    genus = genus.get_level(5)

    pie_data_other = other.get_dict_of_counter()
    pie_data_family = family.get_dict_of_counter()
    pie_data_genus = genus.get_dict_of_counter()


    # %%
    # Plot
    first_fig7, ax1 = plt.subplots(figsize=(12,7))

    m = pd.Series(pie_data_other, pie_data_other.keys()).sort_values(ascending = False)
    l = {}
    c = 0
    last = -1
    l["Others"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l[i[3:]] = m[i]
            l["Others"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l["Others"] = sum(m) - l["Others"]

    first_fig7.set_facecolor("w")
    first_fig7.suptitle("Percentage of taxonomies assigned at the Phylum level of uSGBs\nthat have at least 5 MAGs", color = ('brown'), fontsize = 16, fontweight = "bold")

    plot = sb.barplot(
        x = [item * 100 / other.get_counter() for item in list(l.values())],
        y = list(l.keys()),
        ax = ax1,
        palette = sb.color_palette("inferno_r", 15)
    )

    for i, bar in enumerate(plot.patches):
        ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2., list(l.values())[i], ha = "center", va = "center")
    ax1.set_xlabel("Percentage")
    ax1.set_ylabel("Phylum")

    steps += 1

    plt.tight_layout()

    # Plot
    first_fig8, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,7))

    m = pd.Series(pie_data_family, pie_data_family.keys()).sort_values(ascending = False)
    l1 = {}
    l2 = {}
    c = 0
    last = -1
    l2["Top 10"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l1[i[3:]] = m[i]
            l2["Top 10"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l2["Others"] = sum(m) - l2["Top 10"]

    myexplode = []
    for i in l2.keys():
        if i == "Others":
            myexplode.append(0.2)
        else:
            myexplode.append(0)

    first_fig8.set_facecolor("w")
    first_fig8.suptitle("Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs", color = ('brown'), fontsize = 16, fontweight = "bold")
    ax1.pie(
        x = [item / family.get_counter() for item in list(l2.values())],
        labels = list(l2.keys()),
        autopct = "%.2f",
        explode = myexplode,
        colors = sb.color_palette("inferno_r", 15)
    )

    ax2.set_title("Top 10", color = ('g'), fontsize = 12, fontweight = "bold")
    plot = sb.barplot(
        x = [item * 100 / sum(list(l1.values())) for item in list(l1.values())],
        y = list(l1.keys()),
        palette = sb.color_palette("inferno_r", 15),
        ax = ax2
    )

    for i, bar in enumerate(plot.patches):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2., list(l1.values())[i], ha = "center", va = "center")
    ax2.set_xlabel("Percentage")
    ax2.set_ylabel("Family")

    steps += 1
    plt.tight_layout()

    # %%
    # Plot
    first_fig9, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 7))

    m = pd.Series(pie_data_genus, pie_data_genus.keys()).sort_values(ascending = False)
    l1 = {}
    l2 = {}
    c = 0
    last = -1
    l2["Top 10"] = 0

    for i in m.index:
        out = True
        if c < 10:
            l1[i[3:]] = m[i]
            l2["Top 10"] += m[i]
            c += 1
            out = False

        last = m[i]
        
        if out:
            break

    l2["Others"] = sum(m) - l2["Top 10"]

    myexplode = []
    for i in l2.keys():
        if i == "Others":
            myexplode.append(0.2)
        else:
            myexplode.append(0)

    first_fig9.set_facecolor("w")
    first_fig9.suptitle("Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs", color = ('brown'), fontsize = 16, fontweight = "bold")
    ax1.pie(
        x = [item / genus.get_counter() for item in list(l2.values())],
        labels = list(l2.keys()),
        autopct = "%.2f",
        explode = myexplode,
        colors = sb.color_palette("inferno_r", 15)
    )

    ax2.set_title("Top 10", color = ('g'), fontsize = 12, fontweight = "bold")
    plot = sb.barplot(
        x = [item * 100 / sum(list(l1.values())) for item in list(l1.values())],
        y = list(l1.keys()),
        palette = sb.color_palette("inferno_r", 15),
        ax = ax2
    )

    for i, bar in enumerate(plot.patches):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2., list(l1.values())[i], ha = "center", va = "center")

    plt.tight_layout()
    ax2.set_xlabel("Percentage")
    ax2.set_ylabel("Genus")

    steps += 1

    # %%
    # The number of alternative taxonomies for SGB, showing it indipendently by uSGB
    # and kSGB within the same plot.

    plt.close("all")
    first_fig10, ax1 = plt.subplots(figsize = (12,7))

    first_fig10.set_facecolor("w")
    first_fig10.suptitle("Number of kSGBs by the number of alternative taxonomies", color = ('brown'), fontsize = 16, fontweight = "bold")

    test = sgb_new[sgb_new["Unknown"] == "kSGB"]
    test = test[["Number of Alternative taxonomies"]]

    more100 = test[test["Number of Alternative taxonomies"] > 10]
    if 12 not in more100["Number of Alternative taxonomies"]:
        for i in more100.index:
            test["Number of Alternative taxonomies"].at[i] = 12
    else:
        print("error")

    plt.setp(ax1, xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], xticklabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "", "> 10"])
    plot = sb.histplot(data = test, x = "Number of Alternative taxonomies", stat = "density", discrete = True, ax = ax1, color = my_colors["pink_flesh"])
    count = test["Number of Alternative taxonomies"].value_counts()
    for i in range(1, 11):
        if plot.patches[i].get_height() > 0.5:
            c = "white"
        else:
            c = "black"
        
        if i not in count.index:
            plot.text(i, 0.5, str(0), horizontalalignment = 'center', color = c)
        else:
            plot.text(i, 0.5, str(count[i]), horizontalalignment = 'center', color = c)
    plot.text(12, 0.5, str(count[12]), horizontalalignment = 'center', color = c)

    steps += 1
    plt.tight_layout()

    # %%
    # The proportion of genomes assigned to the assigned taxonomy for each SGB (only
    # for kSGBs). This information can be retrieved from the "List of alternative
    # taxonomies" column. That column contain a list of taxonomies (separated by comma)
    # with the number of reference genomes of the SGB assigned to such taxonomy.

    test = df_new[df_new["Unknown"] == "kSGB"]
    test = test[test["Number of Alternative taxonomies"] > 1]
    proportions_l = []

    for i in test.index:
        if test.loc[i]["Number of Alternative taxonomies"] > 1:
            proportions_l.append(
                int(
                    test.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[1]
                ) / (
                    test.loc[i]["Number of reference genomes"]
                )
            )

    test = pd.DataFrame(
        data = {
            "ID"                                : test["ID"],
            "Number of reference genomes"       : test["Number of reference genomes"],
            "Number of Alternative taxonomies"  : test["Number of Alternative taxonomies"],
            "List of alternative taxonomies"    : test["List of alternative taxonomies"],
            "Proportions"                       : proportions_l
        }
    )

    # Plot "SGB4.jpg"
    plt.close("all")
    first_fig11, ax1 = plt.subplots(figsize=(12,7))

    first_fig11.set_facecolor("w")
    first_fig11.suptitle("Distribution of kSGBs by their proportion of genomes belonging the assigned taxonomy", color = ('brown'), fontsize = 16, fontweight = "bold")

    plot = sb.histplot(data = test, x = "Proportions", stat = "density", ax = ax1, palette = "brg")
    ax1.set_xlabel("Proportion of the genomes belonging to the assigned taxonomy")
    for i, bar in enumerate(plot.patches):
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.3, f"{bar.get_height():.1f}%", ha = "center", va = "center", rotation = 45)

    steps += 1
    plt.tight_layout()

    # %%
    # For the last plot of the percentages of the alternative taxonomies:
    # How many of the SGBs with 50% of the last distribution that only have 2 alternative
    # taxonomies.

    testt = df_new[df_new["Unknown"] == "kSGB"]
    testt = testt[testt["Number of Alternative taxonomies"] > 1]
    testt = pd.merge(testt, test[["ID", "Proportions"]], on = "ID")
    testt = testt[testt["Proportions"] == 0.5]
    testt = testt[testt["Number of Alternative taxonomies"] == 2]

    reg_exp = re.compile(r'(.*(C|c)andidat(e|us)_.*)|(.*_sp(_.*|$))|((.*_|^)(b|B)acterium(_.*|$))|(.*(eury|)archaeo(n_|te).*)|(.*(endo|)symbiont.*|.*genomosp_.* |.*unidentified.*|.*_bacteria_.*|.*_taxon_.*|.*_et_al_.*|.*_and_.*|.*(cyano|proteo|actino)bacterium_.*)')

    a = 0
    b = 0
    c = 0

    sgb5_bin = pd.DataFrame(columns = ["ID", "Assigned", "Assigned Genomes", "Alternative", "Alternative Genomes"])
    sgb5_nbin = pd.DataFrame(columns = ["ID", "Assigned", "Assigned Genomes", "Alternative", "Alternative Genomes"])
    sgb5_binNbin = pd.DataFrame(columns = ["ID", "Assigned", "Assigned Genomes", "Alternative", "Alternative Genomes"])

    bin_type = ""
    df_out = pd.DataFrame(columns = ["ID", "Type", "List of alternative taxonomies"])

    for i in testt.index:
        if reg_exp.match(testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[0].split("|")[6]):
            x = True
        else:
            x = False

        if reg_exp.match(testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[0].split("|")[6]):
            y = True
        else:
            y = False
        
        # non-Binary : non-Binary
        if x & y:
            bin_type = "Non-Binary : Non-Binary"
            c += 1
            sgb5_nbin = pd.concat(
                [
                    sgb5_nbin,
                    pd.DataFrame(
                        data = {
                            "ID"                    : [testt.loc[i]["ID"]],
                            "Assigned"              : [testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[0].split("|")],
                            "Assigned Genomes"      : [testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[1]],
                            "Alternative"           : [testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[0].split("|")],
                            "Alternative Genomes"   : [testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[1]]
                        },
                        index = [i]
                    )
                ]
            )
        # Binary : Binary
        elif not (x | y):
            bin_type = "Binary : Binary"
            a += 1
            sgb5_bin = pd.concat(
                [
                    sgb5_bin,
                    pd.DataFrame(
                        data = {
                            "ID"                    : [testt.loc[i]["ID"]],
                            "Assigned"              : [testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[0].split("|")],
                            "Assigned Genomes"      : [testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[1]],
                            "Alternative"           : [testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[0].split("|")],
                            "Alternative Genomes"   : [testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[1]]
                        },
                        index = [i]
                    )
                ]
            )
        # Binary : non Binary and vice versa
        else:
            bin_type = "Binary : Non-Binary"
            b += 1
            sgb5_binNbin =pd.concat(
                [
                    sgb5_binNbin,
                    pd.DataFrame(
                        data = {
                            "ID"                    : [testt.loc[i]["ID"]],
                            "Assigned"              : [testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[0].split("|")],
                            "Assigned Genomes"      : [testt.loc[i]["List of alternative taxonomies"].split(",")[0].split(":")[1]],
                            "Alternative"           : [testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[0].split("|")],
                            "Alternative Genomes"   : [testt.loc[i]["List of alternative taxonomies"].split(",")[1].split(":")[1]]
                        },
                        index = [i]
                    )
                ]
            )
        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "ID"                                : [testt.loc[i]["ID"]],
                    "Type"                              : [bin_type],
                    "List of alternative taxonomies"    : [testt.loc[i]["List of alternative taxonomies"]]
                }
            )
        ], ignore_index = True)
        
    # Out df
    df_out.to_csv(FILES_const + "df_first_fig12.txt", sep = "\t", index = False)
    del df_out
        
    testt = pd.DataFrame(
        data = {
            "Binary : Binary"         : [a],
            "Binary : Non-Binary"     : [b],
            "Non-Binary : Non-Binary" : [c]
        }
    )

    # Plot "SGB5.jpg"
    plt.close("all")
    first_fig12, ax1 = plt.subplots(figsize = (12,7))

    first_fig12.set_facecolor("w")
    first_fig12.suptitle("SGBs with 2 alternative taxonomies in a 50 / 50 proportion", color = ('brown'), fontsize = 16, fontweight = "bold")
    plot = sb.barplot(data = testt, ax = ax1, palette = [my_colors["magenta"], my_colors["lilla"], my_colors["sky"]])
    ax1.set_xlabel("Group")
    ax1.set_ylabel("Number of SGBs")

    plot.text(0, plot.patches[0].get_height() / 2., str(testt.loc[0]["Binary : Binary"]), horizontalalignment = 'center')
    plot.text(1, plot.patches[1].get_height() / 2., str(testt.loc[0]["Binary : Non-Binary"]), horizontalalignment = 'center')
    plot.text(2, plot.patches[2].get_height() / 2., str(testt.loc[0]["Non-Binary : Non-Binary"]), horizontalalignment = 'center')

    steps += 1
    plt.tight_layout()

    # %%
    # Binary:Binary -> how many are from different genus, different family .... until the kingdom

    bin_type = ""
    df_out = pd.DataFrame(columns = ["A", "ID"])

    l_t = [0 for i in range(7)]
    for i in sgb5_bin.index:
        for j in range(7):
            if sgb5_bin.loc[i]["Assigned"][j] != sgb5_bin.loc[i]["Alternative"][j]:
                l_t[j] += 1
                break
        if j == 0:
            bin_type = "Kingdom"
        elif j == 1:
            bin_type = "Phylum"
        elif j == 2:
            bin_type = "Class"
        elif j == 3:
            bin_type = "Order"
        elif j == 4:
            bin_type = "Family"
        elif j == 5:
            bin_type = "Genus"
        elif j == 6:
            bin_type = "Same Genus"
        
        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "A" : [bin_type],
                    "ID"                 : [sgb5_bin.loc[i]["ID"]]
                }
            )
        ], ignore_index = True)

    df_out = pd.merge(pd.read_csv(FILES_const + "df_first_fig12.txt", sep = "\t"), df_out, how = "left", on ="ID")
    df_out.to_csv(FILES_const + "df_first_fig12.txt", sep = "\t", index = False)
    del df_out

    # Plot "SGB6.jpg"
    plt.close("all")
    first_fig13, ax1 = plt.subplots(figsize = (12,7))

    first_fig13.set_facecolor("w")
    first_fig13.suptitle("Number of SGBs by the higher taxonomic level that differs\nbetween the to alternative taxonomies. `Binary : Binary` group", color = ('brown'), fontsize = 16, fontweight = "bold")
    test = pd.DataFrame(
            {
                "lab" : ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Same Genus"],
                "val" : l_t
            }
        )

    plot = sb.barplot(
        data = test,
        x = "lab",
        y = "val",
        ax = ax1,
        palette = [
            my_colors["purple"],        # Kingdom
            my_colors["light_blue"],    # Phylum
            my_colors["cyan"],          # Class
            my_colors["green"],         # Order
            my_colors["lime"],          # Family
            my_colors["orange"],        # Genus
            my_colors["red"]            # Same Genus
        ]
    )
    plot.set(xlabel = "Taxonomic level")
    plot.set(ylabel = "Number of SGBs")

    for i in range(len(test)):
        plot.text(i, plot.patches[i].get_height() / 2., str(l_t[i]), horizontalalignment = 'center')

    steps += 1
    plt.tight_layout()

    # %%
    # Binary : non-Binary -> how many are from different genus, different family .... until the kingdom

    df_out = pd.DataFrame(columns = ["B", "ID"])

    l_t = [0 for i in range(7)]
    for i in sgb5_binNbin.index:
        for j in range(7):
            if sgb5_binNbin.loc[i]["Assigned"][j] != sgb5_binNbin.loc[i]["Alternative"][j]:
                l_t[j] += 1
                break
        if j == 0:
            bin_type = "Kingdom"
        elif j == 1:
            bin_type = "Phylum"
        elif j == 2:
            bin_type = "Class"
        elif j == 3:
            bin_type = "Order"
        elif j == 4:
            bin_type = "Family"
        elif j == 5:
            bin_type = "Genus"
        elif j == 6:
            bin_type = "Same Genus"
        
        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "B" : [bin_type],
                    "ID"                 : [sgb5_binNbin.loc[i]["ID"]]
                }
            )
        ], ignore_index = True)

    df_out = pd.merge(pd.read_csv(FILES_const + "df_first_fig12.txt", sep = "\t"), df_out, how = "left", on ="ID")
    df_out.to_csv(FILES_const + "df_first_fig12.txt", sep = "\t", index = False)
    del df_out

    # Plot "SGB6.jpg"
    plt.close("all")
    first_fig14, ax1 = plt.subplots(figsize = (12,7))

    first_fig14.set_facecolor("w")
    first_fig14.suptitle("Number of SGBs by the higher taxonomic level that differs\nbetween the to alternative taxonomies. `Binary : Non-Binary` group", color = ('brown'), fontsize = 16, fontweight = "bold")
    test = pd.DataFrame(
            {
                "lab" : ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Same Genus"],
                "val" : l_t
            }
        )

    plot = sb.barplot(
        data = test,
        x = "lab",
        y = "val",
        ax = ax1,
        palette = [
            my_colors["purple"],        # Kingdom
            my_colors["light_blue"],    # Phylum
            my_colors["cyan"],          # Class
            my_colors["green"],         # Order
            my_colors["lime"],          # Family
            my_colors["orange"],        # Genus
            my_colors["red"]            # Same Genus
        ]
    )
    plot.set(xlabel = "Taxonomic level")
    plot.set(ylabel = "Number of SGBs")

    for i in range(len(test)):
        plot.text(i, plot.patches[i].get_height() / 2., str(l_t[i]), horizontalalignment = 'center')

    steps += 1
    plt.tight_layout()

    # %%
    # non-Binary: non-Binary -> how many are from different genus, different family .... until the kingdom

    df_out = pd.DataFrame(columns = ["C", "ID"])

    l_t = [0 for i in range(7)]
    for i in sgb5_nbin.index:
        for j in range(7):
            if sgb5_nbin.loc[i]["Assigned"][j] != sgb5_nbin.loc[i]["Alternative"][j]:
                l_t[j] += 1
                break
        if j == 0:
            bin_type = "Kingdom"
        elif j == 1:
            bin_type = "Phylum"
        elif j == 2:
            bin_type = "Class"
        elif j == 3:
            bin_type = "Order"
        elif j == 4:
            bin_type = "Family"
        elif j == 5:
            bin_type = "Genus"
        elif j == 6:
            bin_type = "Same Genus"
        
        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "C" : [bin_type],
                    "ID"                 : [sgb5_nbin.loc[i]["ID"]]
                }
            )
        ], ignore_index = True)

    df_out = pd.merge(pd.read_csv(FILES_const + "df_first_fig12.txt", sep = "\t"), df_out, how = "left", on ="ID")
    df_out["AB"] = df_out["A"].fillna(df_out["B"])
    df_out["End Taxonomy Level"] = df_out["AB"].fillna(df_out["C"])
    df_out = df_out[["ID", "Type", "End Taxonomy Level", "List of alternative taxonomies"]]

    df_out.to_csv(FILES_const + "df_first_fig12.txt", sep = "\t", index = False)

    f = open(PAGES_const + "df_first_fig12.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "ID | Type | End Taxonomy Level | List of alternative taxonomies\n" +
        "------------ | ------------- | ------------- | -------------\n"
    )

    for row in df_out.index:
        for column in list(df_out.columns)[:-1]:
            f.write(str(df_out.loc[row][column]) + "\t| ")
        f.write(str(df_out.loc[row][list(df_out.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    temp = df_out[df_out["Type"] == "Binary : Binary"]
    f = open(PAGES_const + "df_first_fig13.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "ID | Type | End Taxonomy Level | List of alternative taxonomies\n" +
        "------------ | ------------- | ------------- | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-1]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    temp = df_out[df_out["Type"] == "Binary : Non-Binary"]
    f = open(PAGES_const + "df_first_fig14.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "ID | Type | End Taxonomy Level | List of alternative taxonomies\n" +
        "------------ | ------------- | ------------- | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-1]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    temp = df_out[df_out["Type"] == "Non-Binary : Non-Binary"]
    f = open(PAGES_const + "df_first_fig15.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "ID | Type | End Taxonomy Level | List of alternative taxonomies\n" +
        "------------ | ------------- | ------------- | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-1]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    del df_out, temp

    # Plot "SGB6.jpg"
    plt.close("all")
    first_fig15, ax1 = plt.subplots(figsize = (12,7))

    first_fig15.set_facecolor("w")
    first_fig15.suptitle("Number of SGBs by the higher taxonomic level that differs\nbetween the to alternative taxonomies. `Non-Binary : Non-Binary` group", color = ('brown'), fontsize = 16, fontweight = "bold")
    test = pd.DataFrame(
            {
                "lab" : ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Same Genus"],
                "val" : l_t
            }
        )

    plot = sb.barplot(
        data = test,
        x = "lab",
        y = "val",
        ax = ax1,
        palette = [
            my_colors["purple"],        # Kingdom
            my_colors["light_blue"],    # Phylum
            my_colors["cyan"],          # Class
            my_colors["green"],         # Order
            my_colors["lime"],          # Family
            my_colors["orange"],        # Genus
            my_colors["red"]            # Same Genus
        ]
    )
    plot.set(xlabel = "Taxonomic level")
    plot.set(ylabel = "Number of SGBs")

    for i in range(len(test)):
        plot.text(i, plot.patches[i].get_height() / 2., str(l_t[i]), horizontalalignment = 'center')

    steps += 1
    plt.tight_layout()

    # %%
    # For each FGB in the SGB table-> we create the FGB-GGB-SGB tree:

    fgb = df_new[df_new["Label"] == "FGB"]
    fgb = fgb[fgb["Number of Alternative taxonomies"] > 1]
    fgb = fgb.set_index("ID")
    ggb = df_new[df_new["Label"] == "GGB"]
    ggb = ggb.set_index("ID")
    sgb_new = df_new[df_new["Label"] == "SGB"]
    sgb_new = sgb_new.set_index("ID")

    fgs_gb_tree = mc.Tree()
    for i in fgb[fgb["Unknown"] == "kFGB"].index:
        l1 = fgb.loc[i]["List of reconstructed genomes"].split(",")
        fgs_gb_tree.add_child(path = ["FGB" + str(i)], init = True)
        fgs_gb_tree.children["FGB" + str(i)].customVariables["Assigned taxonomy"] = fgb.loc[i]["Assigned taxonomy"].split("|")
        for j in l1:
            l2 = ggb.loc[int(j[3:])]["List of reconstructed genomes"].split(",")
            fgs_gb_tree.add_child(path = ["FGB" + str(i), j], init = True)
            fgs_gb_tree.children["FGB" + str(i)].children[j].customVariables["Assigned taxonomy"] = ggb.loc[int(j[3:])]["Assigned taxonomy"].split("|")
            for k in l2:
                fgs_gb_tree.add_child(path = ["FGB" + str(i), j, k], init = True)
                fgs_gb_tree.children["FGB" + str(i)].children[j].children[k].customVariables["Assigned taxonomy"] = sgb_new.loc[int(k[3:])]["Assigned taxonomy"].split("|")

    # %%
    # The FGBs with more than 1 f__XXXX (bar plot with the proportion of both groups, those that
    # have more and those that do not; and a list of those that have more than 1)

    family_level = fgs_gb_tree.get_level_list(0)                        # Lista degli FGB (Tree structure)
    family_set = set()                                                  # Set per la lista delle famiglie per ogni FGB
    family_dict = dict()                                                # Dict per conservare il numero di famiglie per ogni FGB

    df_out = pd.DataFrame(columns = ["FGB ID", "Number of Families", "Family names"])

    for x in family_level:                                              # Per ogni FGB
        l = ""
        family_set.clear()
        sgb_level = x.get_level_list(1)                                 # Lista degli SGB per ogni FGB

        for y in sgb_level:                                             # Per ogni SGB aggiungo al Set la famiglia di appartenenza
            family_set.add(y.customVariables["Assigned taxonomy"][4])
        family_dict[x.get_name()] = len(family_set)                     # Salva il count delle famiglie nel FGB

        if len(family_set) > 1:                                         # Stampa l'output per FGB con più famiglie
            for y in family_set:
                l = l + str(y) + ","        
        else:                                                           # Stampa l'output per FGB con 1 famiglia
            for y in family_set:
                l = l + str(y) + ","

        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "FGB ID"                : [x.get_name()],
                    "Number of Families"    : [len(family_set)],
                    "Family names"          : [l[:-1]]
                }
            )
        ], ignore_index = True)

    df_out.to_csv(FILES_const + "df_first_fig16.txt", sep = "\t", index = False)

    f = open(PAGES_const + "df_first_fig16.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "FGB ID | Number of Families | Family names\n" +
        "------------ | ------------- | -------------\n"
    )

    for row in df_out.index:
        for column in list(df_out.columns)[:-1]:
            f.write(str(df_out.loc[row][column]) + "\t| ")
        f.write(str(df_out.loc[row][list(df_out.columns)[-1]]).replace(",", ", ") + "\n")
    f.close()

    temp = df_out[df_out["Number of Families"] > 1]
    f = open(PAGES_const + "df_first_fig16_more1.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "FGB ID | Number of Families | Family names\n" +
        "------------ | ------------- | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-2]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]).replace(",", ", ") + "\n")
    f.close()

    temp = df_out[df_out["Number of Families"] == 1]
    f = open(PAGES_const + "df_first_fig16_only1.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "FGB ID | Family names\n" +
        "------------ | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-1]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]) + "\n")
    f.close()

    del df_out, temp

    family_dict_1 = dict()                                              # Dict che contiene count = 1 in family_dict per il plot
    family_dict_2 = dict()                                              # Dict che contiene count > 1 in family_dict per il plot
    for x in family_dict:
        if family_dict[x] > 1:
            family_dict_2[x] = family_dict[x]
        else:
            family_dict_1[x] = 1

    # Plot "FGB1_family.jpg"
    first_fig16, ax1 = plt.subplots(figsize = (12,7))

    first_fig16.set_facecolor("w")
    first_fig16.suptitle("Taxonomic families per FGB", color = ('brown'), fontsize = 16, fontweight = "bold")
    plot = sb.barplot(x = ["FGB that have only 1 family", "FGB that have more than 1 families"], y = [len(family_dict_1), len(family_dict_2)], ax = ax1)
    plot.text(0, plot.patches[0].get_height() / 2., str(len(family_dict_1)), horizontalalignment = 'center')
    plot.text(1, plot.patches[1].get_height() / 2., str(len(family_dict_2)), horizontalalignment = 'center')
    plot.set(xlabel = "Group")
    plot.set(ylabel = "Number of FGBs")

    steps += 1
    plt.tight_layout()

    # %%
    # The g__ that are in more than 1 FGB (bar plot with the proportion of both groups, those that
    # have more and those that do not; and a list of those that have more than 1)

    genus_level = fgs_gb_tree.get_level_list(1)
    genus_dict = {}
    for i in genus_level:
        s1 = "|".join(i.customVariables["Assigned taxonomy"][:5])       # "Kingdom|Phylum|Class|Order|Family"
        s2 = i.customVariables["Assigned taxonomy"][5]                  # "Genus"

        if s2 not in genus_dict.keys():                                 # Inizializza i dizionari in modo dict[dict[...], dict[...], ...]
            genus_dict[s2] = dict()

        if s1 in genus_dict[s2]:                                        # Qui si ha la struttura del tipo dict[dict[int], dict[int], ...]
            genus_dict[s2][s1] += 1
        else:
            genus_dict[s2][s1] = 1

    count = 0
    genus_pie = dict()                                                  # Dict che contiene il numero di volte che compare la chiave
    for i in genus_dict:
        if (len(genus_dict[i]) > 1) or (list(genus_dict[i].values())[0] > 1):
            if i not in genus_pie:
                genus_pie[i] = 0
            for j in genus_dict[i]:
                count += genus_dict[i][j]                               # Conta tutti i geni totali
                genus_pie[i] += genus_dict[i][j]

    df_out = pd.DataFrame(columns = ["Genus", "Number of different taxonomies", "Different taxonomies"])

    for key in genus_dict:
        l = ""
        ccount = 0
        value = genus_dict[key]
        valuel = list(value.values())[0]
        if (len(value) > 1) or (valuel > 1):
            if len(value) == 1:
                for key2 in value:
                    value2 = value[key2]
                    l = l + str(key2) + ":" + str(value2) + ","
                    ccount += 1
            elif len(value) > 1:
                for key2 in value:
                    value2 = value[key2]
                    l = l + str(key2) + ":" + str(value2) + ","
                    ccount += 1
            
            df_out = pd.concat([
                df_out,
                pd.DataFrame(
                    data = {
                        "Genus"                             : [str(key)],
                        "Number of different taxonomies"    : [ccount],
                        "Different taxonomies"              : [l[:-1]]
                    }
                )
            ], ignore_index = True)

    df_out.to_csv(FILES_const + "df_first_fig17.txt", sep = "\t", index = False)

    f = open(PAGES_const + "df_first_fig17.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "Genus | Number of different taxonomies | Different taxonomies\n" +
        "------------ | ------------- | -------------\n"
    )

    for row in df_out.index:
        for column in list(df_out.columns)[:-1]:
            f.write(str(df_out.loc[row][column]) + "\t| ")
        f.write(str(df_out.loc[row][list(df_out.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    temp = df_out[df_out["Number of different taxonomies"] > 1]
    f = open(PAGES_const + "df_first_fig17_more1.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "Genus | Number of different taxonomies | Different taxonomies\n" +
        "------------ | ------------- | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-1]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    temp = df_out[df_out["Number of different taxonomies"] == 1]
    f = open(PAGES_const + "df_first_fig17_only1.md", "w")
    f.write(
        "# Table containing the SGB concerned\n" +
        "Genus | Different taxonomies\n" +
        "------------ | -------------\n"
    )

    for row in temp.index:
        for column in list(temp.columns)[:-2]:
            f.write(str(temp.loc[row][column]) + "\t| ")
        f.write(str(temp.loc[row][list(temp.columns)[-1]]).replace("|", "\|") + "\n")
    f.close()

    del df_out, temp

    # Plot "FGB2_genus.jpg"
    first_fig17, ax1 = plt.subplots(figsize = (12,7))

    first_fig17.set_facecolor("w")
    first_fig17.suptitle("Taxonomic genera present in several FGBs", color = ('brown'), fontsize = 16, fontweight = "bold")
    plot = sb.barplot(x = ["Genus in only 1 FGB", "Genus in more than 1 FGB"], y = [len(genus_level) - count, count], ax = ax1)
    plot.text(0, plot.patches[0].get_height() / 2., str(len(genus_level) - count), horizontalalignment = 'center')
    plot.text(1, plot.patches[1].get_height() / 2., count, horizontalalignment = 'center')
    plot.set(xlabel = "Group")
    plot.set(ylabel = "Number of genera")

    sgb_new = df_new[df_new["Label"] == "SGB"]

    steps += 1
    plt.tight_layout()

    # %%
    if len(files) - 1 == index_file:
        reg_exp_list = [                                                                    # Lista delle espressioni regolari
            re.compile(r'.*(C|c)andidat(e|us)_.*'),
            re.compile(r'.*_sp(_.*|$)'),
            re.compile(r'(.*_|^)(b|B)acterium(_.*|$)'),
            re.compile(r'.*(eury|)archaeo(n_|te).*'),
            re.compile(r'.*(endo|)symbiont.*'),
            re.compile(r'.*genomosp_.*'),
            re.compile(r'.*unidentified.*'),
            re.compile(r'.*unclassified.*'),
            re.compile(r'.*_bacteria_.*'),
            re.compile(r'.*_taxon_.*'),
            re.compile(r'.*_et_al_.*'),
            re.compile(r'.*_and_.*'),
            re.compile(r'.*(cyano|proteo|actino)bacterium_.*')
        ]

        # For each SGB with more than 1 alternative taxonomy:
        # 1. We get all the alternative taxonomies of the SGB up to the g__ level
        # 2. We check which is the g__ with more genomes after applying the penalisation for the
        #    taxonomies (up to the g__) that pass the reg. expression
        # 3. With the wining g__, we assign the taxonomy to the SGB with only the genomes belonging to
        #    that g__ by also applying the penalisation for the taxonomies that pass the reg. expression
        # 4. For the taxonomies that now are different than in the original table, we report them in
        #    a table

        more1_original = sgb_new[sgb_new["Unknown"] == "kSGB"]                          #       Tabella originale
        more1_original = more1_original[more1_original["Number of Alternative taxonomies"] > 1]

        more1_modified = sgb_new[sgb_new["Unknown"] == "kSGB"]                          #       Tabella modificata finale
        more1_modified = more1_modified[more1_modified["Number of Alternative taxonomies"] > 1]

        SGB_modified = set()                                                    #       Set contenente lista degli index degli SGB modificati
        SGB_ID_dict = dict()
        SGB_modified_dict = dict()                                              #       Dict per la visualizzazione nell'editor
        SGB_original_dict = dict()                                              #       Dict per la visualizzazione nell'editor

        res_list = dict()                                                       #       Dict per la visualizzazione del risultato nell'editor
        groupby = dict()                                                        #       Dict per selezione del g__ migliore per ogni SGB

        for i in more1_modified.index:                                          # (1)   Per ogni SGB
            target_max = -float('inf')                                          #       Massimo per la selezione in groupby
            target = list()                                                     #       g__ selezionato in groupby

            maxx = -float('inf')                                                #       Massimo (inclusa penalità) per decidere la migliore tassonomia
            real_maxx = -float('inf')                                           #       Numero di genomi reale
            tax = "Null"                                                        #       Tassonomia migliore selezionata
            alt_tax = more1_modified.loc[i]["List of alternative taxonomies"].split(",")    # Lista delle tassonomie alternative (list)

            groupby.clear()
            for x in alt_tax:                                                   #       Raggruppo le alt tax del tipo g__ con il numero tot di genomi
                if x.split(":")[0].split("|")[5] in groupby:
                    groupby[x.split(":")[0].split("|")[5]] += int(x.split(":")[1])
                else:
                    groupby[x.split(":")[0].split("|")[5]] = int(x.split(":")[1])
            
            for x in sorted(groupby):                                           #       Seleziona migliore g__ in ordine alfabetico applicando la penalità
                penality = apply_penality_str(x, reg_exp_list)
                if groupby[x] - penality > target_max:
                    target_max = groupby[x] - penality
                    target.clear()
                    target.append(x)
                elif groupby[x] - penality == target_max:
                    target.append(x)
            
            target_alt_tax = list()
            for x in alt_tax:                                                   #       Seleziona le tassonomie alternative in base al target selezionato
                if x.split(":")[0].split("|")[5] in target:
                    target_alt_tax.append(x)

            for x in sorted(target_alt_tax):                                            # (2)   Controlla ogni tax alt e applica la penalità
                penality = apply_penality_tax(x, 6, reg_exp_list)

                if int(x.split(":")[1]) - penality > maxx:                      #       Applico la penalità e controllo se è il massimo
                    maxx = int(x.split(":")[1]) - penality
                    real_maxx = int(x.split(":")[1])
                    tax = x.split(":")[0]
                    
            res_list[i] = tax + ":" + str(int(real_maxx))

            x = "|".join(more1_modified.loc[i]["Assigned taxonomy"].split(":")[0].split("|")[:7])
            if x != tax:                                                        # (3)   Se è diverso dall'originale lo modifica con quello nuovo
                SGB_modified.add(i)
                more1_modified.at[i,"Assigned taxonomy"] = "|".join([tax, "|".join(more1_original.loc[i]["Assigned taxonomy"].split(":")[0].split("|")[7:])])
                SGB_ID_dict[i] = more1_modified.loc[i]["ID"]
                SGB_modified_dict[i] = more1_modified.loc[i]["Assigned taxonomy"]
                SGB_original_dict[i] = more1_original.loc[i]["Assigned taxonomy"]

        ass_tax_modif = pd.DataFrame(                                           # (4)   Crea tabella con le differenze tra originale e modificato
            data = {
                "ID"                    : list(SGB_ID_dict.values()),
                "Old assigned taxonomy" : list(SGB_original_dict.values()),
                "New assigned taxonomy" : list(SGB_modified_dict.values())
            },
            index = list(SGB_modified_dict.keys())
        )

        ass_tax_modif.to_csv(FILES_const + "df_first_modified.txt", sep = "\t", index = False)

        f = open(PAGES_const + "df_first_modified.md", "w")
        f.write(
            "# Table containing the SGB concerned\n" +
            "ID | Old assigned taxonomy | New assigned taxonomy\n" +
            "------------ | ------------- | -------------\n"
        )

        for row in ass_tax_modif.index:
            for column in list(ass_tax_modif.columns)[:-1]:
                f.write(str(ass_tax_modif.loc[row][column]).replace("|", "\|") + "\t| ")
            f.write(str(ass_tax_modif.loc[row][list(ass_tax_modif.columns)[-1]]).replace("|", "\|") + "\n")
        f.close()

        steps += 1
        plt.tight_layout()

    # %%

    if index_file > 0:
        test = pd.DataFrame(
            data = {
                "Unknown"       : sgb_new["Unknown"].value_counts().index,
                PAST_FILE_const[:5] : sgb_old["Unknown"].value_counts(),
                FILE_const[:5]      : sgb_new["Unknown"].value_counts()
            },
            index = sgb_new["Unknown"].value_counts().index
        )

        plt.close("all")
        second_fig1, ax1 = plt.subplots(figsize = (12,7))

        second_fig1.set_facecolor("w")
        second_fig1.suptitle("How many SGBs are new", color = ('brown'), fontsize = 16, fontweight = "bold")
        plot = sb.barplot(data = pd.melt(test, id_vars = ["Unknown"], value_vars = [PAST_FILE_const[:5], FILE_const[:5]]), x = "Unknown", y = "value", hue = "variable", ax = ax1)
        plot.text(-0.2, len(sgb_old[sgb_old["Unknown"] == "uSGB"]) / 2, str(len(sgb_old[sgb_old["Unknown"] == "uSGB"])), horizontalalignment = 'center')
        plot.text(0.2, len(sgb_new[sgb_new["Unknown"] == "uSGB"]) / 2, str(len(sgb_new[sgb_new["Unknown"] == "uSGB"])), horizontalalignment = 'center')
        plot.text(0.8, len(sgb_old[sgb_old["Unknown"] == "kSGB"]) / 2, str(len(sgb_old[sgb_old["Unknown"] == "kSGB"])), horizontalalignment = 'center')
        plot.text(1.2, len(sgb_new[sgb_new["Unknown"] == "kSGB"]) / 2, str(len(sgb_new[sgb_new["Unknown"] == "kSGB"])), horizontalalignment = 'center')
        plot.set(xlabel = "SGB type")
        plot.set(ylabel = "Number of SGBs")

        steps += 1
        plt.tight_layout()

        # %%
        # [3] Comparing an old and a new version
        # 
        # How many uSGBs became kSGBs in the new version. And the other way around

        sgb_old3 = pd.DataFrame(
            data = sgb_old[["ID", "Assigned taxonomy", "Unknown"]]
        )

        sgb_new3 = pd.DataFrame(
            data = sgb_new[["ID", "Assigned taxonomy", "Unknown"]]
        )

        sgb_comparison_merged = pd.merge(sgb_old3, sgb_new3, on = "ID", suffixes = ["_old", "_new"])

        df_out = pd.DataFrame(columns = ["ID", "Old assigned taxonomy", "New assigned taxonomy", "Type of change"])
        upgrade = 0
        downgrade = 0
        for i in sgb_comparison_merged.index:
            if (sgb_comparison_merged.loc[i]["Unknown_old"] == "uSGB") & (sgb_comparison_merged.loc[i]["Unknown_new"] == "kSGB"):
                upgrade += 1
                df_out = pd.concat([
                    df_out,
                    pd.DataFrame(
                        data = {
                            "ID"                    : [sgb_comparison_merged.loc[i]["ID"]],
                            "Old assigned taxonomy" : [sgb_comparison_merged.loc[i]["Assigned taxonomy_old"]],
                            "New assigned taxonomy" : [sgb_comparison_merged.loc[i]["Assigned taxonomy_new"]],
                            "Type of change"        : ["From uSGB to kSGB"]
                        }
                    )
                ])
            elif (sgb_comparison_merged.loc[i]["Unknown_old"] == "kSGB") & (sgb_comparison_merged.loc[i]["Unknown_new"] == "uSGB"):
                downgrade += 1
                df_out = pd.concat([
                    df_out,
                    pd.DataFrame(
                        data = {
                            "ID"                    : [sgb_comparison_merged.loc[i]["ID"]],
                            "Old assigned taxonomy" : [sgb_comparison_merged.loc[i]["Assigned taxonomy_old"]],
                            "New assigned taxonomy" : [sgb_comparison_merged.loc[i]["Assigned taxonomy_new"]],
                            "Type of change"        : ["From kSGB to uSGB"]
                        }
                    )
                ])

        df_out.to_csv(FILES_const + "df_second_fig2.txt", sep = "\t", index = False)

        f = open(PAGES_const + "df_second_fig2.md", "w")
        f.write(
            "# Table containing the SGB concerned\n" +
            "ID | Old assigned taxonomy | New assigned taxonomy | Type of change\n" +
            "------------ | ------------- | ------------- | -------------\n"
        )

        for row in df_out.index:
            for column in list(df_out.columns)[:-1]:
                f.write(str(df_out.loc[row][column]).replace("|", "\|") + "\t| ")
            f.write(str(df_out.loc[row][list(df_out.columns)[-1]]) + "\n")
        f.close()

        f = open(PAGES_const + "df_second_fig2_upgrade.md", "w")
        f.write(
            "# Table containing the SGB concerned\n" +
            "ID | Old assigned taxonomy | New assigned taxonomy\n" +
            "------------ | ------------- | -------------\n"
        )

        test = df_out[df_out["Type of change"] == "From uSGB to kSGB"]
        for row in df_out.index:
            for column in list(df_out.columns)[:-2]:
                f.write(str(df_out.loc[row][column]).replace("|", "\|") + "\t| ")
            f.write(str(df_out.loc[row][list(df_out.columns)[-2]]).replace("|", "\|") + "\n")
        f.close()

        f = open(PAGES_const + "df_second_fig2_downgrade.md", "w")
        f.write(
            "# Table containing the SGB concerned\n" +
            "ID | Old assigned taxonomy | New assigned taxonomy\n" +
            "------------ | ------------- | -------------\n"
        )

        test = df_out[df_out["Type of change"] == "From kSGB to uSGB"]
        for row in df_out.index:
            for column in list(df_out.columns)[:-2]:
                f.write(str(df_out.loc[row][column]).replace("|", "\|") + "\t| ")
            f.write(str(df_out.loc[row][list(df_out.columns)[-2]]).replace("|", "\|") + "\n")
        f.close()

        del df_out, test

        
        # %%
        # Tab

        other = mc.Tree()
        family = mc.Tree()
        genus = mc.Tree()
        species = mc.Tree()

        for i in sgb_old.index:
            l = sgb_old.loc[i]["Assigned taxonomy"].split(",")[0].split(":")[0].split("|")
            if sgb_old.loc[i]["Level of assigned taxonomy"] == "Other":
                other.add_child(path = l, init = True)
            elif sgb_old.loc[i]["Level of assigned taxonomy"] == "Family":
                family.add_child(path = l, init = True)
            elif sgb_old.loc[i]["Level of assigned taxonomy"] == "Genus":
                genus.add_child(path = l, init = True)
            elif sgb_old.loc[i]["Level of assigned taxonomy"] == "Species":
                species.add_child(path = l, init = True)

        other = other.get_level(1)
        family = family.get_level(4)
        genus = genus.get_level(5)
        species = species.get_level(6)

        pie_data_other = other.get_dict_of_counter()
        pie_data_family = family.get_dict_of_counter()
        pie_data_genus = genus.get_dict_of_counter()
        pie_data_species = species.get_dict_of_counter()

        # Phylum
        m = pd.Series(pie_data_other, pie_data_other.keys()).sort_values(ascending = False)
        l_other_old = {}
        c = 0
        last = -1
        l_other_old["Others"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l_other_old[i[3:]] = m[i]
                l_other_old["Others"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        l_other_old["Others"] = sum(m) - l_other_old["Others"]
        temp_out = l_other_old.pop("Others")

        l_other_old = [(l_other_old[i], i.replace("_", " ")) for i in l_other_old.keys()]
        l_other_old.sort(key = lambda tup: tup[1], reverse = False)
        l_other_old.sort(key = lambda tup: tup[0], reverse = True)
        
        l_other_old.append((temp_out, "Others"))

        # Family
        m = pd.Series(pie_data_family, pie_data_family.keys()).sort_values(ascending = False)
        l_family_old = {}
        c = 0
        last = -1
        l_family_old["Others"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l_family_old[i[3:]] = m[i]
                l_family_old["Others"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        l_family_old["Others"] = sum(m) - l_family_old["Others"]
        temp_out = l_family_old.pop("Others")
        
        l_family_old = [(l_family_old[i], i.replace("_", " ")) for i in l_family_old.keys()]
        l_family_old.sort(key = lambda tup: tup[1], reverse = False)
        l_family_old.sort(key = lambda tup: tup[0], reverse = True)
        
        l_family_old.append((temp_out, "Others"))

        # Genus
        m = pd.Series(pie_data_genus, pie_data_genus.keys()).sort_values(ascending = False)
        l_genus_old = {}
        c = 0
        last = -1
        l_genus_old["Others"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l_genus_old[i[3:]] = m[i]
                l_genus_old["Others"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        l_genus_old["Others"] = sum(m) - l_genus_old["Others"]
        temp_out = l_genus_old.pop("Others")
        
        l_genus_old = [(l_genus_old[i], i.replace("_", " ")) for i in l_genus_old.keys()]
        l_genus_old.sort(key = lambda tup: tup[1], reverse = False)
        l_genus_old.sort(key = lambda tup: tup[0], reverse = True)

        l_genus_old.append((temp_out, "Others"))

        # Species
        m = pd.Series(pie_data_species, pie_data_species.keys()).sort_values(ascending = False)
        l_species_old = {}
        c = 0
        last = -1
        l_species_old["Others"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l_species_old[i[3:]] = m[i]
                l_species_old["Others"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        l_species_old["Others"] = sum(m) - l_species_old["Others"]
        temp_out = l_species_old.pop("Others")
        
        l_species_old = [(l_species_old[i], i.replace("_", " ")) for i in l_species_old.keys()]
        l_species_old.sort(key = lambda tup: tup[1], reverse = False)
        l_species_old.sort(key = lambda tup: tup[0], reverse = True)

        l_species_old.append((temp_out, "Others"))

        # Plot "Comparison_Old_New_3.jpg"
        plt.close("all")
        second_fig2, ax1 = plt.subplots(figsize = (12,7))

        second_fig2.set_facecolor("w")
        second_fig2.suptitle("How many SGBs change type", color = ('brown'), fontsize = 16, fontweight = "bold")
        plot = sb.barplot(data = pd.DataFrame({"From uSGB to kSGB" : [upgrade], "From kSGB to uSGB" : [downgrade]}), ax = ax1)
        plot.set(xlabel = "Type of change")
        plot.set(ylabel = "Number of SGBs")

        plot.text(0, upgrade / 2, str(upgrade), horizontalalignment = 'center')
        plot.text(1, downgrade / 2, str(downgrade), horizontalalignment = 'center')

        steps += 1
        plt.tight_layout()

        # %%
        # [4b] Comparing an old and a new version
        # 
        # The pieplots from the last time (SGB9b), but comparing old and new version

        sgb_new4b = sgb_new[sgb_new["Number of reconstructed genomes"] > 4]
        sgb_new4b = sgb_new4b[sgb_new4b["Unknown"] == "uSGB"]
        sgb_old4b = sgb_old[sgb_old["Number of reconstructed genomes"] > 4]
        sgb_old4b = sgb_old4b[sgb_old4b["Unknown"] == "uSGB"]

        # Old
        tree_old = mc.Tree()
        other_old = mc.Tree()
        family_old = mc.Tree()
        genus_old = mc.Tree()

        for i in sgb_old4b.index:
            l = sgb_old4b.loc[i]["Assigned taxonomy"].split(",")[0].split(":")[0].split("|")
            if sgb_old4b.loc[i]["Level of assigned taxonomy"] == "Other":
                other_old.add_child(path = l, init = True)
            elif sgb_old4b.loc[i]["Level of assigned taxonomy"] == "Family":
                family_old.add_child(path = l, init = True)
            elif sgb_old4b.loc[i]["Level of assigned taxonomy"] == "Genus":
                genus_old.add_child(path = l, init = True)
            
            tree_old.add_child(path = l, init = True)

        other_old = other_old.get_level(1)
        family_old = family_old.get_level(4)
        genus_old = genus_old.get_level(5)

        pie_data_other_old = other_old.get_dict_of_counter()
        pie_data_family_old = family_old.get_dict_of_counter()
        pie_data_genus_old = genus_old.get_dict_of_counter()

        # New
        tree_new = mc.Tree()
        other_new = mc.Tree()
        family_new = mc.Tree()
        genus_new = mc.Tree()

        for i in sgb_new4b.index:
            l = sgb_new4b.loc[i]["Assigned taxonomy"].split(",")[0].split(":")[0].split("|")
            if sgb_new4b.loc[i]["Level of assigned taxonomy"] == "Other":
                other_new.add_child(path = l, init = True)
            elif sgb_new4b.loc[i]["Level of assigned taxonomy"] == "Family":
                family_new.add_child(path = l, init = True)
            elif sgb_new4b.loc[i]["Level of assigned taxonomy"] == "Genus":
                genus_new.add_child(path = l, init = True)
            
            tree_new.add_child(path = l, init = True)

        other_new = other_new.get_level(1)
        family_new = family_new.get_level(4)
        genus_new = genus_new.get_level(5)

        pie_data_other_new = other_new.get_dict_of_counter()
        pie_data_family_new = family_new.get_dict_of_counter()
        pie_data_genus_new = genus_new.get_dict_of_counter()

        # Plot "Comparison_Old_New_4B_other.jpg"
        second_fig3, ax1 = plt.subplots(figsize = (12,7))

        m = pd.Series(pie_data_other_new, pie_data_other_new.keys(), dtype = "object").sort_values(ascending = False)
        l = {}
        c = 0
        last = -1
        l["Others"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l[i[3:]] = m[i]
                l["Others"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        l["Others"] = sum(m) - l["Others"]
        l2 = l

        df_out = pd.DataFrame(
            data = {
                "Phylum"        : list(l.keys()),
                "Percentage"    : [item * 100 / other_new.get_counter() for item in list(l.values())],
                "Value"         : [str(item) + " / " + str(other_new.get_counter()) for item in list(l.values())],
                "Version"       : [FILE_const[:5]] * len(l.values()),
                "Index"         : [len(l.values()) - i for i in range(len(l.values()))]
            }
        )

        m = pd.Series(pie_data_other_old, pie_data_other_old.keys(), dtype = "object").sort_values(ascending = False)
        l = {}
        c = 0
        last = -1
        l["Others"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l[i[3:]] = m[i]
                l["Others"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        l["Others"] = sum(m) - l["Others"]

        index = dict()
        i = 0

        l1 = dict()
        for x in l.keys():
            if x in l2.keys():
                l1[x] = l[x]
                
        for x in l2.keys():
            if x not in l1.keys():
                if ("p__" + x) in m:
                    l1[x] = m["p__" + x]
                else:
                    l1[x] = 0
            
            index[x] = l1[x]

        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "Phylum"        : list(index.keys()),
                    "Percentage"    : [item * 100 / max(1, other_old.get_counter()) for item in list(index.values())],
                    "Value"         : [str(item) + " / " + str(other_old.get_counter()) for item in list(index.values())],
                    "Version"       : [PAST_FILE_const[:5]] * len(index.values()),
                    "Index"         : [len(index.values()) - i for i in range(len(index.values()))]
                }
            )
        ], ignore_index = True)

        second_fig3.set_facecolor("w")
        second_fig3.suptitle("Percentage of taxonomies assigned at the Phylum level of uSGBs that have at least 5 MAGs", color = ('brown'), fontsize = 16, fontweight = "bold")



        df_out["Sorting"] = df_out["Version"].apply(lambda x: int(x[3:5]) * 100 + MAPPING_MONTH[x[:3]])
        df_out = df_out.sort_values(by = ["Index", "Sorting"], ascending = False, axis = 0)
        df_out = df_out[["Phylum", "Percentage", "Value", "Version"]]
        # print(df_out)

        plot = sb.barplot(
            data = df_out,
            x = "Percentage",
            y = "Phylum",
            hue = "Version",
            ax = ax1,
            palette = sb.color_palette("inferno_r")
        )

        for i, bar in enumerate(plot.patches):
            ax1.text(bar.get_width() + 3, bar.get_y() + bar.get_height() / 2., df_out.loc[i]["Value"], ha = "center", va = "center")
        
        plt.legend(loc = "lower right")

        steps += 1
        plt.tight_layout()

        # %%
        # Plot "Comparison_Old_New_4B_family.jpg"
        second_fig4= plt.figure(figsize = (12, 11))
        ax1 = second_fig4.add_subplot(221)
        ax2 = second_fig4.add_subplot(222)
        ax3 = second_fig4.add_subplot(212)

        second_fig4.set_facecolor("w")
        second_fig4.suptitle("Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs", color = ('brown'), fontsize = 16, fontweight = "bold")

        # New
        m = pd.Series(pie_data_family_new, pie_data_family_new.keys()).sort_values(ascending = False)
        l = {}
        ll = {}
        c = 0
        last = -1
        ll["Top 10"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l[i[3:]] = m[i]
                ll["Top 10"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        ll["Others"] = sum(m) - ll["Top 10"]
        l2 = l

        df_out = pd.DataFrame(
            data = {
                "Phylum"        : list(l.keys()),
                "Percentage"    : [item * 100 / family_new.get_counter() for item in list(l.values())],
                "Value"         : [str(item) + " / " + str(family_new.get_counter()) for item in list(l.values())],
                "Version"       : [FILE_const[:5]] * len(l.values()),
                "Index"         : [len(l.values()) - i for i in range(len(l.values()))]
            }
        )

        myexplode = []
        for i in ll.keys():
            if i == "Others":
                myexplode.append(0.2)
            else:
                myexplode.append(0)

        ax2.set_title(FILE_const[:5], color = ('g'), fontsize = 12, fontweight = "bold")
        ax2.pie(
            x = [item / family_new.get_counter() for item in list(ll.values())],
            labels = list(ll.keys()),
            autopct = "%.2f",
            explode = myexplode,
            colors = [(0.981173, 0.759135, 0.156863), (0.633998, 0.168992, 0.383704)]
        )

        # Old
        m = pd.Series(pie_data_family_old, pie_data_family_old.keys(), dtype = "object").sort_values(ascending = False)
        l = {}
        ll = {}
        c = 0
        last = -1
        ll["Top 10"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l[i[3:]] = m[i]
                ll["Top 10"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        ll["Others"] = sum(m) - ll["Top 10"]

        index = dict()
        i = 0

        l1 = dict()
        for x in l.keys():
            if x in l2.keys():
                l1[x] = l[x]
                
        for x in l2.keys():
            if (x not in l1.keys()) and (("f__" + x) in m.keys()):
                l1[x] = m["f__" + x]
            
            if ("f__" + x) in m.keys():
                index[x] = l1[x]
            else:
                index[x] = 0
                
        if PAST_FILE_const[:5] == "None":
            PAST_FILE_const = "NaN00"

        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "Phylum"        : list(index.keys()),
                    "Percentage"    : [item * 100 / max(1, family_old.get_counter()) for item in list(index.values())],
                    "Value"         : [str(item) + " / " + str(family_old.get_counter()) for item in list(index.values())],
                    "Version"       : [PAST_FILE_const[:5]] * len(index.values()),
                    "Index"         : [len(index.values()) - i for i in range(len(index.values()))]
                }
            )
        ], ignore_index = True)
        
        if PAST_FILE_const[:5] == "NaN00":
            PAST_FILE_const = "None"

        myexplode = []
        for i in ll.keys():
            if i == "Others":
                myexplode.append(0.2)
            else:
                myexplode.append(0)

        ax1.set_title(PAST_FILE_const[:5], color = ('g'), fontsize = 12, fontweight = "bold")
        ax1.pie(
            x = [item / max(1, family_old.get_counter()) for item in list(ll.values())],
            labels = list(ll.keys()),
            autopct = "%.2f",
            explode = myexplode,
            colors = [(0.961293, 0.488716, 0.084289), (0.434987, 0.097069, 0.432039)]
        )

        df_out["Sorting"] = df_out["Version"].apply(lambda x: int(x[3:5]) * 100 + MAPPING_MONTH[x[:3]])
        df_out = df_out.sort_values(by = ["Index", "Sorting"], ascending = False, axis = 0)
        df_out = df_out[["Phylum", "Percentage", "Value", "Version"]]
        # print(df_out)

        plot = sb.barplot(
            data = df_out,
            x = "Percentage",
            y = "Phylum",
            hue = "Version",
            ax = ax3,
            palette = sb.color_palette("inferno_r")
        )

        for i, bar in enumerate(plot.patches):
            ax3.text(bar.get_width() + 0.7, bar.get_y() + bar.get_height() / 2., df_out.loc[i]["Value"], ha = "center", va = "center")

        plt.legend(loc = "lower right")

        steps += 1
        plt.tight_layout()

        # %%
        # Plot "Comparison_Old_New_4B_genus.jpg"
        second_fig5 = plt.figure(figsize = (12, 11))
        ax1 = second_fig5.add_subplot(221)
        ax2 = second_fig5.add_subplot(222)
        ax3 = second_fig5.add_subplot(212)

        second_fig5.set_facecolor("w")
        second_fig5.suptitle("Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs", color = ('brown'), fontsize = 16, fontweight = "bold")

        # Old
        m = pd.Series(pie_data_genus_new, pie_data_genus_new.keys()).sort_values(ascending = False)
        l = {}
        ll = {}
        c = 0
        last = -1
        ll["Top 10"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l[i[3:]] = m[i]
                ll["Top 10"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        ll["Others"] = sum(m) - ll["Top 10"]
        l2 = l

        df_out = pd.DataFrame(
            data = {
                "Phylum"        : list(l.keys()),
                "Percentage"    : [item * 100 / genus_new.get_counter() for item in list(l.values())],
                "Value"         : [str(item) + " / " + str(genus_new.get_counter()) for item in list(l.values())],
                "Version"       : [FILE_const[:5]] * len(l.values()),
                "Index"         : [len(l.values()) - i for i in range(len(l.values()))]
            }
        )

        myexplode = []
        for i in ll.keys():
            if i == "Others":
                myexplode.append(0.2)
            else:
                myexplode.append(0)

        ax2.set_title(FILE_const[:5], color = ('g'), fontsize = 12, fontweight = "bold")
        ax2.pie(
            x = [item / genus_new.get_counter() for item in list(ll.values())],
            labels = list(ll.keys()),
            autopct = "%.2f",
            explode = myexplode,
            colors = [(0.981173, 0.759135, 0.156863), (0.633998, 0.168992, 0.383704)]
        )

        # Old
        m = pd.Series(pie_data_genus_old, pie_data_genus_old.keys(), dtype = "object").sort_values(ascending = False)
        l = {}
        ll = {}
        c = 0
        last = -1
        ll["Top 10"] = 0

        for i in m.index:
            out = True
            if c < 10:
                l[i[3:]] = m[i]
                ll["Top 10"] += m[i]
                c += 1
                out = False

            last = m[i]
            
            if out:
                break

        ll["Others"] = sum(m) - ll["Top 10"]

        index = dict()
        i = 0

        l1 = dict()
        for x in l.keys():
            if x in l2.keys():
                l1[x] = l[x]
                
        for x in l2.keys():
            if (x not in l1.keys()) and (("f__" + x) in m.keys()):
                l1[x] = m["f__" + x]
            
            if ("f__" + x) in m.keys():
                index[x] = l1[x]
            else:
                index[x] = 0
        
        if PAST_FILE_const[:5] == "None":
            PAST_FILE_const = "NaN00"

        df_out = pd.concat([
            df_out,
            pd.DataFrame(
                data = {
                    "Phylum"        : list(index.keys()),
                    "Percentage"    : [item * 100 / max(1, genus_old.get_counter()) for item in list(index.values())],
                    "Value"         : [str(item) + " / " + str(genus_old.get_counter()) for item in list(index.values())],
                    "Version"       : [PAST_FILE_const[:5]] * len(index.values()),
                    "Index"         : [len(index.values()) - i for i in range(len(index.values()))]
                }
            )
        ], ignore_index = True)
        
        if PAST_FILE_const[:5] == "NaN00":
            PAST_FILE_const = "None"

        myexplode = []
        for i in ll.keys():
            if i == "Others":
                myexplode.append(0.2)
            else:
                myexplode.append(0)

        ax1.set_title(PAST_FILE_const[:5], color = ('g'), fontsize = 12, fontweight = "bold")
        ax1.pie(
            x = [item / max(1, genus_old.get_counter()) for item in list(ll.values())],
            labels = list(ll.keys()),
            autopct = "%.2f",
            explode = myexplode,
            colors = [(0.961293, 0.488716, 0.084289), (0.434987, 0.097069, 0.432039)]
        )

        df_out["Sorting"] = df_out["Version"].apply(lambda x: int(x[3:5]) * 100 + MAPPING_MONTH[x[:3]])
        df_out = df_out.sort_values(by = ["Index", "Sorting"], ascending = False, axis = 0)
        df_out = df_out[["Phylum", "Percentage", "Value", "Version"]]

        plot = sb.barplot(
            data = df_out,
            x = "Percentage",
            y = "Phylum",
            hue = "Version",
            ax = ax3,
            palette = sb.color_palette("inferno_r")
        )

        for i, bar in enumerate(plot.patches):
            ax3.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2., df_out.loc[i]["Value"], ha = "center", va = "center")

        plt.legend(loc = "lower right")
        steps += 1
        plt.tight_layout()

    # %%
    first_fig1.savefig(PICTURES_const + "first_fig1.jpg")
    first_fig2.savefig(PICTURES_const + "first_fig2.jpg")
    first_fig3.savefig(PICTURES_const + "first_fig3.jpg")
    first_fig4.savefig(PICTURES_const + "first_fig4.jpg")
    first_fig5.savefig(PICTURES_const + "first_fig5.jpg")
    first_fig6.savefig(PICTURES_const + "first_fig6.jpg")
    first_fig7.savefig(PICTURES_const + "first_fig7.jpg")
    first_fig8.savefig(PICTURES_const + "first_fig8.jpg")
    first_fig9.savefig(PICTURES_const + "first_fig9.jpg")
    first_fig10.savefig(PICTURES_const + "first_fig10.jpg")
    first_fig11.savefig(PICTURES_const + "first_fig11.jpg")
    first_fig12.savefig(PICTURES_const + "first_fig12.jpg")
    first_fig13.savefig(PICTURES_const + "first_fig13.jpg")
    first_fig14.savefig(PICTURES_const + "first_fig14.jpg")
    first_fig15.savefig(PICTURES_const + "first_fig15.jpg")
    first_fig16.savefig(PICTURES_const + "first_fig16.jpg")
    first_fig17.savefig(PICTURES_const + "first_fig17.jpg")

    
    f = open(RELEASES + FILE_const[:5] + "/" + FILE_const[:5] + ".md", "w")
    f.write(
        "# Report for the " + FILE_const[:5] + " release\n" +
        "## Releases overview\n\n\n" +
        "Release | Total MAGs | Total Reference Genomes | New MAGs | New Reference Genomes | Total kSGBs | Total uSGBs | New kSGBs | New uSGBs | Unknown to known\n" +
        "------------ | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------\n"
    )

    for row in tab.index:
        f.write("[" + str(tab.loc[row]["Release"]) + "](../" + str(tab.loc[row]["Release"]) + "/" + str(tab.loc[row]["Release"]) + ".md)\t| ")
        for column in list(tab.columns)[1:-1]:
            f.write(str(tab.loc[row][column]) + "\t| ")
        f.write(str(tab.loc[row][list(tab.columns)[-1]]) + "\n")
        if str(tab.loc[row]["Release"]) == FILE_const[:5]:
            break

    f.write(
        # Intro Tab
        "\n## " + FILE_const[:5] + " release overview\n\n\n" +
        "Level | Bacteria | Archaea | Eukaryota | Total\n" +
        "------------ | ------------- | ------------- | ------------- | -------------\n"
    )

    for row in tab_sgb_lev.index:
        f.write(str(row) + "\t| ")
        for column in list(tab_sgb_lev.columns)[:-1]:
            f.write(str(tab_sgb_lev.loc[row][column]) + "\t| ")
        f.write(str(tab_sgb_lev.loc[row][list(tab_sgb_lev.columns)[-1]]) + "\n")
    f.write("\n\n")

    f.write(
        # first_fig1
        "Histogram showing the number of `kSGBs`, `uSGBs`, `reconstructed` and `reference genomes` included in " + FILE_const[:5] + "\n\n" +
        "![Number of kSGBs, uSGBs, reconstructed and reference genomes](" + PICTURES + "first_fig1.jpg)\n\n\n" +

        # first_fig2
        "Histogram showing the number of **NEW** `kSGBs`, `uSGBs`, `reconstructed` and `reference genomes` included in " + FILE_const[:5] + "\n\n" +
        "![Number of NEW kSGBs, uSGBs, reconstructed and reference genomes](" + PICTURES + "first_fig2.jpg)\n\n\n" +

        # first_fig3
        "## Distribution of the kSGBs by number of genomes in the database\n" +
        "Histograms showing the distribution density of kSGBs by the number of genomes in the database. " +
        "In particular, the number of kSGBs that have respectively from 0 to 10 reconstructed and reference genomes are shown. " +
        "In the 12th column there is a grouping of all the others with more than 10.\n\n" +
        "![The number of genomes for each kSGB](" + PICTURES + "first_fig3.jpg)\n\n\n" +

        # first_fig4
        "## Distribution of the uSGBs by number of genomes in the database\n" +
        "Histograms showing the distribution density of uSGBs by the number of genomes in the database. " +
        "In particular, the number of uSGBs that have respectively from 0 to 10 reconstructed and reference genomes are shown. " +
        "In the 12th column there is a grouping of all the others with more than 10.\n\n" +
        "![The number of genomes for each uSGB](" + PICTURES + "first_fig4.jpg)\n\n\n" +

        # first_fig5
        "## Number of SGBs by the level of assigned taxonomy\n" +
        "Histogram showing the number of SGBs by their lower level of known taxonomy.\n\n" +
        "![Number of SGBs by the level of assigned taxonomy](" + PICTURES + "first_fig5.jpg)\n\n\n" +

        # tab_first_fig5
        "<table><tr><th colspan = '2' style = 'text-align: center'>Phylum</th><th colspan = '2' style = 'text-align: center'>Family</th><th colspan = '2' style = 'text-align: center'>Genus</th><th colspan = '2' style = 'text-align: center'>Species</th></tr><tr><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th><th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th></tr>"
    )

    for i_tab_first_fig5 in range(11):
        fin = ""
        if i_tab_first_fig5 == 10:
            fin = " style = 'font-weight: bold'"
        
        f.write("<tr" + fin + ">")
        
        f.write("<td>")
        f.write(str(l_other[i_tab_first_fig5][1]))
        f.write("</td>")
        f.write("<td>")
        f.write(str(l_other[i_tab_first_fig5][0]))
        f.write("</td>")
        
        f.write("<td>")
        f.write(str(l_family[i_tab_first_fig5][1]))
        f.write("</td>")
        f.write("<td>")
        f.write(str(l_family[i_tab_first_fig5][0]))
        f.write("</td>")
        
        f.write("<td>")
        f.write(str(l_genus[i_tab_first_fig5][1]))
        f.write("</td>")
        f.write("<td>")
        f.write(str(l_genus[i_tab_first_fig5][0]))
        f.write("</td>")

        f.write("<td>")
        f.write(str(l_species[i_tab_first_fig5][1]))
        f.write("</td>")
        f.write("<td>")
        f.write(str(l_species[i_tab_first_fig5][0]))
        f.write("</td>")

        f.write("</tr>")
    f.write("</table>\n\n")

    f.write(
        # first_fig6
        "## Number of uSGBs with, at least 5 MAGs, by the level of assigned taxonomy\n" +
        "Histogram showing the number of uSGBs, with at least 5 MAGs in the database, by their lower level of known taxonomy.\n\n" +
        "![Number of uSGBs with, at least, 5 MAGs by the level of assigned taxonomy](" + PICTURES + "first_fig6.jpg)\n\n\n" +

        # first_fig7
        "## Taxonomies assigned at the Phylum level for uSGBs with, at least, 5 MAGs\n" +
        "Percentage of uSGBs with, at least, 5 MAGs assigned to different phylum.\n\n" +
        "![Percentage of taxonomies assigned at the Phylum level of uSGBs that have at least 5 MAGs](" + PICTURES + "first_fig7.jpg)\n\n\n" +
        
        # first_fig8
        "## Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs\n" +
        "Percentage of uSGBs with, at least, 5 MAGs assigned to different families. " +
        "The top 10 assigned families are shown in the histogram in the right.\n\n" +
        "![Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs](" + PICTURES + "first_fig8.jpg)\n\n\n" +

        # first_fig9
        "## Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs\n" +
        "Percentage of uSGBs with, at least, 5 MAGs assigned to different genus. " +
        "The top 10 assigned genus are shown in the histogram in the right.\n\n" +
        "![Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs](" + PICTURES + "first_fig9.jpg)\n\n\n" +

        # first_fig10
        "## Number of alternative taxonomies for the kSGBs\n" +
        "Histogram representing the distribution of kSGBs by the number of alternative taxonomies. \n\n" +
        "![Number of kSGBs by the number of the alternative taxonomies](" + PICTURES + "first_fig10.jpg)\n\n\n" +

        # first_fig11
        "## Distribution of kSGBs by their proportion of reference genomes belonging to the assigned taxonomy\n" +
        "Histogram showing the distribution of kSGBs by the proportion of the reference genomes belonging " +
        "to the assigned taxonomy.\n\n" +
        "![Distribution of kSGBs by their proportion of genomes belonging the assigned taxonomy](" + PICTURES + "first_fig11.jpg)\n\n\n" +

        # first_fig12
        "## SGBs with 2 alternative taxonomies in a 50 / 50 proportion\n" +
        "Histogram reporting the SGBs with 2 alternative taxonomies in a 50 / 50 genomes proportion. We defined 3 groups: " +
        "\"Binary : Binary\", \"Binary : Non-Binary\" and \"Non-Binary : Non-Binary\". " +
        "Binary we mean that the taxonomy respects the criteria values set by the regular " +
        "expression reported here \" `(.*(C|c)andidat(e|us)_.*)|(.*_sp(_.*|$))|((.*_|^)(b|B)acterium(_.*|$))|" +
        "(.*(eury|)archaeo(n_|te).*)|(.*(endo|)symbiont.*|.*genomosp_.* |.*unidentified.*|.*_bacteria_.*|." +
        "*_taxon_.*|.*_et_al_.*|.*_and_.*|.*(cyano|proteo|actino)bacterium_.*)` \", while Non-Binary " +
        "mean the opposite.\n\n" +
        "### [Here](" + PAGES + "df_first_fig12.md) you can see the list of SGBs.\n\n" +
        "![SGBs with 2 alternative taxonomies in a 50 / 50 proportion](" + PICTURES + "first_fig12.jpg)\n\n" +

        # first_fig13
        "## Taxonomic differences in the alternative taxonomies for the SGBs with 2 alternative taxonomues in a 50 / 50 proporyion\n" +
        "Histogram showing, for the `Binary : Binary` group the number of SGBs by the higher taxonomic " +
        "level that differs between the two alternative taxonomies.\n\n" +
        "### [Here](" + PAGES + "df_first_fig13.md) you can see the list of SGBs.\n\n" +
        "![Number of SGBs by the higher taxonomic level that differs between the to alternative taxonomies. `Binary : Binary` group](" + PICTURES + "first_fig13.jpg)\n\n\n" +

        # first_fig14
        "The same as the previous one applies to this but with `Binary : Non-Binary` (obiously also the complementary one).\n\n" +
        "### [Here](" + PAGES + "df_first_fig14.md) you can see the list of SGBs.\n\n" +
        "![Number of SGBs by the higher taxonomic level that differs between the to alternative taxonomies. `Binary : Non-Binary` group](" + PICTURES + "first_fig14.jpg)\n\n\n" +

        # first_fig15
        "The same as the previous one applies to this but with `Non-Binary : Non-Binary`.\n\n" +
        "### [Here](" + PAGES + "df_first_fig15.md) you can see the list of SGBs.\n\n" +
        "![Number of SGBs by the higher taxonomic level that differs between the to alternative taxonomies. `Non-Binary : Non-Binary` group](" + PICTURES + "first_fig15.jpg)\n\n\n" +

        # first_fig16
        "## Taxonomic families per FGB\n" +
        "This graph shows the number of families present in a single FGB. The first column shows the number " +
        "of FGBs that have associated only one family, while the second shows thos that have " +
        "that associated more than one.\n\n" +
        "![Taxonomic families per FGB](" + PICTURES + "first_fig16.jpg)\n\n" +
        "### [Here](" + PAGES + "df_first_fig16.md) the list of FGBs with their families\n\n" +
        "### [Here](" + PAGES + "df_first_fig16_more1.md) the list of FGBs with more than one family\n\n" +
        "### [Here](" + PAGES + "df_first_fig16_only1.md) the list of FGBs with only one familiy\n\n" +
    
        # first_fig17
        "## Taxonomic genera present in several FGBs\n" +
        "Histogram showing the number of genera appearing in one or more FGBs. " +
        "In the first column there are the number of those that appear " +
        "only in one FGB, while in the second those that appear in more than one.\n\n" +
        "![Taxonomic genera present in several FGBs](" + PICTURES + "first_fig17.jpg)\n\n" +
        "### [Here](" + PAGES + "df_first_fig17.md) the list of FGBs with their genus\n\n" +
        "### [Here](" + PAGES + "df_first_fig17_more1.md) the list of FGBs with more than one genus\n\n" +
        "### [Here](" + PAGES + "df_first_fig17_only1.md) the list of FGBs with only one genus\n\n"
    )

    if len(files) - 1 == index_file:
        f.write(
            # SGB taxonomies modified
            "## Assigning taxonomy based on a majority rule accounting for the main genera\n" +
            "[Here](" + PAGES + "df_first_modified.md) is the list of SGB whose taxonomy could be replaced with a new assigning method.\n\n"

            # SGB statistics table
            "## Table containing the statistics for the current version\n" +
            "The table contains several statistics between one SGB and the others.\n" +
            "The complete list is [Here](" + PAGES + "df_first_statistics_table.md).\n\n"
        )

        # f_s = open(FILES_const + "df_first_statistics_table.txt","w")
        # f_s.write(
        #     "SGB\t" +
        #     "Number of genomes\t" +
        #     "Average distance\t" +
        #     "Max distance\t" +
        #     "Min distance\t" +
        #     "Max average distance of rows\t" +
        #     "Min average distance of rows\t" +
        #     "Number of outliers\n"
        # )

        # lines = os.listdir('/shares/CIBIO-Storage/CM/scratch/databases/MetaRefSGB/releases')
        # for lineNumber, file_in_lines in enumerate(lines):        
        #     # Percorso del file da aprire
        #     file_s = "/shares/CIBIO-Storage/CM/scratch/databases/MetaRefSGB/pwd/" + FILE_const[:5] + "/" + file_in_lines[:-1]
            
        #     # Settaggio del DataFrame del file
        #     df_s = pd.read_csv(file_s, sep = "\t")
        #     df_s = df_s.rename(columns = {"Unnamed: 0": ""})
        #     df_s = df_s.set_index("")
            
        #     if (len(df_s.index) > 1):
        #         # Settaggio delle variabili necessarie
        #         avgg_s = 0.0                  # Average distance
        #         maxx_s = 0.0                  # Max distance
        #         minn_s = float('inf')         # Min distance
        #         avgg_max_s = 0.0              # Max average distance of rows
        #         avgg_min_s = float('inf')     # Min average distance of rows
        #         counter_avgg_max_s = 0        # Number of outliers

        #         # Lettura del DataFrame del file
        #         for i in df_s.index:                 # Per ogni riga
        #             avgg_rel_s = 0.0                     # Media per riga
                    
        #             for j in df_s.index:                 # Per ogni colonna
        #                 value_s = df_s.loc[i][j]               # Ignora diagonale
        #                 if i != j:
        #                     avgg_s += value_s                  # avg parziale
        #                     avgg_rel_s += value_s
        #                     if value_s > maxx_s:               # max
        #                         maxx_s = value_s
        #                     if value_s < minn_s:               # min
        #                         minn_s = value_s
                    
        #             avgg_rel_s /= len(df_s.index) - 1
                    
        #             if avgg_rel_s > avgg_max_s:            # max avg per riga
        #                 avgg_max_s = avgg_rel_s
        #             if avgg_rel_s < avgg_min_s:            # min avg per riga
        #                 avgg_min_s = avgg_rel_s
        #             if avgg_rel_s > 0.05:                # n° outliers
        #                 counter_avgg_max_s += 1

        #         avgg_s /= len(df_s.index)**2 - len(df_s.index)

        #         # Outputs
        #         f_s.write(
        #             file_in_lines[:-5] + "\t"        # SGB
        #             + str(len(df_s.index)) + "\t"      # Number of genomes
        #             + str(float(avgg_s)) + "\t"        # Average distance
        #             + str(maxx_s) + "\t"               # Max distance
        #             + str(minn_s) + "\t"               # Min distance
        #             + str(avgg_max_s) + "\t"           # Max average distance of rows
        #             + str(avgg_min_s) + "\t"           # Min average distance of rows
        #             + str(counter_avgg_max_s) + "\n"   # Number of outliers
        #         )
        # # End for
        # f_s.close()

        # Output tab completa
        f_out = open(PAGES_const + "df_first_statistics_table.md", "w")
        test = pd.read_csv(FILES_const + "df_first_statistics_table.txt", sep = "\t")
        test = test.sort_values(["Number of outliers"], ascending = False)

        for column in test.columns[:-1]:
            f_out.write(str(column) + " | ")
        f_out.write(str(test.columns[-1]) + "\n")

        for column in test.columns[:-1]:
            f_out.write("------------ | ")
        f_out.write("------------\n")

        for row in test.index:
            f_out.write(str(int(test.loc[row][test.columns[0]])) + "\t| ")
            f_out.write(str(int(test.loc[row][test.columns[1]])) + "\t| ")
            for column in test.columns[2:-1]:
                f_out.write(str(test.loc[row][column]) + "\t| ")
            f_out.write(str(int(test.loc[row][test.columns[-1]])) + "\n")
        f_out.close()

        # Output nel file attuale
        test = test[test["Number of outliers"] > 0]
        
        for column in test.columns[:-1]:
            f.write(str(column) + " | ")
        f.write(str(test.columns[-1]) + "\n")

        for column in test.columns[:-1]:
            f.write("------------ | ")
        f.write("------------\n")

        for row in test.index:
            f.write(str(int(test.loc[row][test.columns[0]])) + "\t| ")
            f.write(str(int(test.loc[row][test.columns[1]])) + "\t| ")
            for column in test.columns[2:-1]:
                f.write(str(test.loc[row][column]) + "\t| ")
            f.write(str(int(test.loc[row][test.columns[-1]])) + "\n")

    f.close()

    steps += 1

    # %%
    if index_file > 0:
        second_fig1.savefig(PICTURES_const + "second_fig1.jpg")
        second_fig2.savefig(PICTURES_const + "second_fig2.jpg")
        second_fig3.savefig(PICTURES_const + "second_fig3.jpg")
        second_fig4.savefig(PICTURES_const + "second_fig4.jpg")
        second_fig5.savefig(PICTURES_const + "second_fig5.jpg")

        f = open(RELEASES + FILE_const[:5] + "/" + PAST_FILE_const[:5] + "-" + FILE_const[:5] + "_comparison.md", "w")

        f.write(
            "# Comparisons between version " + FILE_const[:5] + " and " + PAST_FILE_const[:5] + "\n" +
            "In this document there are statistics to compare the releases " + FILE_const[:5] + " and " + PAST_FILE_const[:5] + ".\n\n\n" +

            # second_fig1
            "## How many SGBs are new\n" +
            "Histogram showing the number of uSGBs and kSGBs between " + FILE_const[:5] + " and " + PAST_FILE_const[:5] + ".\n\n" +
            "![How many SGBs are new](" + PICTURES + "second_fig1.jpg)\n\n\n" +

            # second_fig2
            "## How many SGBs change type\n" +
            "Histogram showing the number of kSGBs that change to uSGBs and viceversa from " + PAST_FILE_const[:5] + " and " + FILE_const[:5] + ".\n\n" +
            "![How many SGBs change type](" + PICTURES + "second_fig2.jpg)\n\n\n" +
            "### [Here](" + PAGES + "df_second_fig2.md) the list of SGBs that change SGB type\n\n" +
            "### [Here](" + PAGES + "df_second_fig2_upgrade.md) the list of uSGBs that change to kSGB\n\n" +
            "### [Here](" + PAGES + "df_second_fig2_downgrade.md) the list of kSGBs that change to uSGB\n\n" +

            # tab_second
            "<table><tr><th colspan = '4' style = 'text-align: center'>Phylum</th><th colspan = '4' style = 'text-align: center'>Family</th><th colspan = '4' style = 'text-align: center'>Genus</th><th colspan = '4' style = 'text-align: center'>Species</th></tr>"
        )

        f.write("<tr>")
        for i_tab_first_fig5 in range(4):
            f.write("<th colspan = '2' style = 'text-align: center'>" + PAST_FILE_const[:5] + "</th><th colspan = '2' style = 'text-align: center'>" + FILE_const[:5] + "</th>")
        f.write("</tr>")

        f.write("<tr>")
        for i_ in range(8):
            f.write("<th style = 'text-align: center'>Name</th><th style = 'text-align: center'>Count</th>")
        f.write("</tr>")

        for i_tab_first_fig5 in range(11):
            fin = ""
            if i_tab_first_fig5 == 10:
                fin = " style = 'font-weight: bold'"
            
            f.write("<tr" + fin + ">")

            f.write("<td>")
            f.write(str(l_other_old[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_other_old[i_tab_first_fig5][0]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_other[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_other[i_tab_first_fig5][0]))
            f.write("</td>")
            
            f.write("<td>")
            f.write(str(l_family_old[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_family_old[i_tab_first_fig5][0]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_family[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_family[i_tab_first_fig5][0]))
            f.write("</td>")
            
            f.write("<td>")
            f.write(str(l_genus_old[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_genus_old[i_tab_first_fig5][0]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_genus[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_genus[i_tab_first_fig5][0]))
            f.write("</td>")

            f.write("<td>")
            f.write(str(l_species_old[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_species_old[i_tab_first_fig5][0]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_species[i_tab_first_fig5][1]))
            f.write("</td>")
            f.write("<td>")
            f.write(str(l_species[i_tab_first_fig5][0]))
            f.write("</td>")

            f.write("</tr>")
        f.write("</table>\n\n")

        f.write(
            # second_fig3
            "## Taxonomies assigned at the Phylum level for uSGBs with, at least, 5 MAGs\n" +
            "Percentage of uSGBs with, at least, 5 MAGs assigned to different phylum.\n\n" +
            "![Percentage of taxonomies assigned at the Phylum level of uSGBs that have at least 5 MAGs](" + PICTURES + "second_fig3.jpg)\n\n\n"

            # second_fig4
            "## Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs\n" +
            "Percentage of uSGBs with, at least, 5 MAGs assigned to different families. " +
            "The top 10 assigned families are shown in the histogram in the right.\n\n" +
            "![Taxonomies assigned at the Family level for uSGBs with, at least, 5 MAGs](" + PICTURES + "second_fig4.jpg)\n\n\n" +

            # second_fig5
            "## Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs\n" +
            "Percentage of uSGBs with, at least, 5 MAGs assigned to different genus. " +
            "The top 10 assigned genus are shown in the histogram in the right.\n\n" +
            "![Taxonomies assigned at the Genus level for uSGBs with, at least, 5 MAGs](" + PICTURES + "second_fig5.jpg)\n\n\n"
        )
        f.close()

    PAST_FILE_const = FILE_const

    if script_delete:
        shutil.rmtree(FILES_const[:-1])
        shutil.rmtree(PAGES_const[:-1])
        shutil.rmtree(PICTURES_const[:-1])

    steps += 1
    print("\033[0;92m" + str(index_file + 1) + "/" + str(len(files)) + " - " + FILE_const[:5] + " done!!!\033[0;37m")

print("Done!\n")