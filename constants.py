colors = [
    '#769838',
    '#5CB283',
    '#23949A',
    '#3A7266',
    '#324951',
    '#7F4480',
    '#ED603C',
    '#F1850F',
    '#FFBB33',
    '#C5CD7D',
]

colors_accum = [
    '#5CB283',
    '#5CB283AA',
    '#23949AAA',
    '#23949A',
    '#C5CD7D',
    '#324951AA',
    '#769838',
    '#FFBB33',
    '#ED603C',
    '#324951',
    '#7F4480',
    '#F1850F',
    '#3A7266',

]

colors_transparent = [
    '#769838AA',
    '#5CB283AA',
    '#23949AAA',
    '#3A7266AA',
    '#324951AA',
    '#7F4480AA',
    '#ED603CAA',
    '#F1850FAA',
    '#FFBB33AA',
    '#C5CD7DAA',
]

indicators = [
    'GWP',
    'ODP',
    'POCP',
    'AP',
    'EP',
    'ADPe',
    'ADPf',
    'PERT',
    'PENRT',
    'RSF',
    'NRSF'
]
# All caps & Jan 2022 & correct order for comp_elect_heat_stacked_indicators
indicators_caps = [
    'GWP',
    'SENR',
    'ADPF',
    'SER',
    'AP',
    'PENR',
    'ODP',
    'EP',
    'ADPE',
    'PER',
    'POCP'
]

## Undersøg hvad den bruges til - hvad dækker 'map' helt nøjagtigt over?
indicator_map = {
    'gwp': 'GWP',
    'odp': 'ODP',
    'pocp': 'POCP',
    'ap': 'AP',
    'ep': 'EP',
    'adpe': 'ADPe',
    'adpf': 'ADPf',
    'pert': 'PERT',
    'penrt': 'PENRT',
    'rsf': 'RSF',
    'nrsf': 'NRSF',
    'petot': 'PEtot',
    'sek': 'Sek'
}

years = [
    '2023',
    '2025',
    '2027',
    '2029',
]

br_years = [
    'BR23',
    'BR25',
    'BR27',
    'BR29',
]

fk_years = [
    'FCO₂-23',
    'FCO₂-25',
    'FCO₂-27',
    'FCO₂-29',
]

reference_indicators = [
    'GWP',
    'ODP',
    'POCP',
    'AP',
    'EP',
    'ADPe',
    'ADPf',
    'PEtot',
    'Sek'
]

dgnb_indicators = [
    'GWP',
    'POCP',
    'AP',
    'EP',
    'ADPf',
    'PEtot'
]

reference_labels = {
    'indicators': reference_indicators,
    'years': years,
    'br_years': br_years,
    'fk_years': fk_years,
    'dgnb': dgnb_indicators,
}

reference_y_labels = {
    'indicators': '#',
    'years': '#',
    'br_years': '%',
    'fk_years': '%',
    'dgnb': '%',
}

reference_titles = {
    'indicators': 'GenDK reference graf (#)', ### er det fordi det er parametrisk/ afhænger af hvad brugeren vælger?
    'years': 'BR og FCO₂ reference graf (GWP)',
    'br_years': 'BR reference graf (GWP)',
    'fk_years': 'FCO₂ reference graf (GWP)',
    'dgnb': 'DGNB reference'
}

reference_legends = {
    'building': 'Aktuel bygning',
    'reference1': 'BR reference',
    'reference2': 'FCO₂ reference',
    'reference3': 'DGNB reference',
    'lower': 'Nedre kvartil',
    'median': 'Median',
    'higher': 'Øvre kvartil',
}

### Test hvordan denne fungerer // sprøg Christian
### Evt lav til svarende til configurationer

reference_color_index = {
    'building': 0,
    'reference1': 1,
    'reference2': 2,
    'reference3': 3,
}

material_labels = {
    'indicators': indicators,
    'years': years,
    'br_years': br_years,
    'fk_years': fk_years,
}

accumulated_line_styles = {
    'total': 'solid',
    'embedded': 'solid',
    'reference': 'solid',
    'operation': 'solid',
    'operation_reference': 'solid',
    'embedded_with_d': 'dotted',
}

accumulated_legends = {
    'total': 'Total',
    'embedded': 'Embedded',
    'reference': 'Reference',
    'operation': 'Operation',
    'operation_reference': 'Operation (reference)',
    'embedded_with_d': 'Embedded incl. D',
}

# label y-axis
# hvad gør .#? gør den det muligt at replace?
indicator_with_units = {
    'gwp': 'GWP [kg CO₂-eq.#]',
    'odp': 'ODP [kg CFC11-eq.#]',
    'pocp': 'POCP [kg ethene-eq.#]',
    'ap': 'AP [kg SO₂-eq.#]',
    'ep': 'EP [kg PO₄³-eq.#]',
    'adpe': 'ADPe [kg Sb-eq.#]',
    'adpf': 'ADPf [MJ#]',
    'pert': 'PERT [MJ#]',
    'penrt': 'PENRT [MJ#]',
    'rsf': 'RSF [MJ#]',
    'nrsf': 'NRSF [MJ#]',
    'petot': 'PEtot [MJ#]',
    'sek': 'Sek [MJ#]',
}


indicator_with_normalized = {
    'gwp': 'Person-eq. GWP',
    'odp': 'Person-eq. ODP',
    'pocp': 'Person-eq. POCP',
    'ap': 'Person-eq. AP',
    'ep': 'Person-eq. EP',
    'adpe': 'Person-eq. ADPe',
    'adpf': 'Person-eq. ADPf',
    'pert': 'Person-eq. PERT',
    'penrt': 'Person-eq. PENRT',
    'rsf': 'Person-eq. RSF',
    'nrsf': 'Person-eq. NRSF',
    'petot': 'Person-eq. PEtot',
    'sek': 'Person-eq. Sek',
}

normalized_indicator_unit = {
    'total': '',
    'm2year': '/m²/year',
    'm2': '/m²',
    'normalized': '',
}

#brug denne
accumulated_title = {
    'total': 'Accumulated total, #',
    'building_and_operation': 'Accumulated embedded and operation, #'
}

stages_labels_stages = [
    'A1-3',
    'A4',
    'A5',
    'B4',
    'B6',
    'C3',
    'C4',
    'D',
    'ExC3',
    'ExC4',
    'ExD',
]

stages_labels_construction_site = [
    'A4 Transport\n(andet)',
    'A4 Transport\n(bygningsdele)',
    'A5 Spild\n(bygningsdele)',
    'A5 El',
    'A5 Varme',
    'A5 Maskiner',
    'A5 Transport'
]

stages_labels_operation = [
    'Electricity',
    'Heating'
]
# Noden nedenfor er tilgøjet terese januar tre-ugers
# Electricity indeholder alle stages nedenfor
# Heating indeholde alle stages nedenfor ekls. D
stages_labels_stages_building_operation = [
    'SumD',
    'Sum',
    'D',
    'SumEx',
    'SumNew',
    'B6'
]

stages_labels = {
    'stages': stages_labels_stages,
    'construction_site': stages_labels_construction_site,
    'operation': stages_labels_operation
}

stages_title = {
    'stages': 'Stages #',
    'construction_site': 'Construction site #',
    'operation': 'Operation #'
}

stages_normalization = {
    'total': 'total (#)',
    'm2': 'pr. m² (#)',
    'm2year': 'pr. m²/year (#)',
    'normalized': 'normalized (#)',
}

embedded_vs_operation_label = {
    '1_embedded': 'Embedded',
    '2_heat': 'Heating',
    '3_electricity': 'Elektricity'
}

replaceable_material_labels = {
    'Mineralske byggematerialer': 'Mineralske\nbyggematerialer',
    'Overfladebehandling og belægning af metaller': 'Overfladebehandling og\nbelægning af metaller',
    'Komponenter til vinduer og glasfacader': 'Komponenter til vinduer\nog glasfacader',
    'Konstruktionstræ, savet og tørret (KVH-kvalitet)': 'Konstruktionstræ,\nsavet og tørret (KVH-kvalitet)',
}

#brug denne
material_levels = {
    'hyper': 'main element category, #',
    'super': 'super element category, #',
    'normal': 'category, #',
}

# Use these
hotspot_levels = {
    'specific': 'specific, #',
    'super': 'super element category, #',
    'category': 'category, #',
    'element': 'element, #',
    'construction': 'construction, #',
    'product': 'product, #',
    'stage': 'stage, #',
}
# Use these
hotspot_titles = {
    'specific': 'specific, #',
    'super': 'Hotspot Element Category (Total)',
    'category': 'Hotspot Category (Total)',
    'element': 'Hotspot Element (Total)',
    'construction': 'Hotspot Construction (Total)',
    'product': 'Hotspot Product (Total)',
    'stage': 'Hotspot Stage (Total)',
}

# Use these
hotspot_titles_all_building = {
    'element': 'Hotspot-analysis of all elements in the building',
    'construction': 'Hotspot-analysis of all constructions in the building',
    'product': 'Hotspot-analysis of all products in the building',
}


scenario_overview_levels = {
    'total': 'total, #',
    'stages': 'faser, #',
    'embedded_and_operation': 'drift mv., #',
}

scenario_overview_color_index = {
    'total': 0,
    'operation': 0,
    'construction_site': 1,
    'embedded': 2,
    'sum': 0,
    'SumNew': 0,
    'sum_d': 1,
    'sumD': 1,
    'a1-3': 0,
    'A1to3': 0,
    'A1-3': 0,
    'a4': 1,
    'A4': 1,
    'a5': 2,
    'A5': 2,
    'b4': 3,
    'B4': 3,
    'b6': 4,
    'B6': 4,
    'c3': 5,
    'ex_c3': 5,
    'C3': 5,
    'c4': 6,
    'ex_c4': 6,
    'C4': 6,
    'd': 9,
    'ex_d': 9,
    'D': 9,
    'ExC3': 5,
    'ExC4': 6,
    'ExD': 9,
}

scenario_overview_legends = {
    'total': 'Total',
    'operation': 'Operation',
    'construction_site': 'Construction site',
    'embedded': 'Elements',
    'a1-3': 'A1-3',
    'A1-3': 'A1-3',
    'A1to3': 'A1-3',
    'a4': 'A4',
    'A4': 'A4',
    'a5': 'A5',
    'A5': 'A5',
    'b4': 'B4',
    'B4': 'B4',
    'b6': 'B6',
    'c3': 'C3',
    'ex_c3': 'Ex. C3',
    'C3': 'C3',
    'c4': 'C4',
    'ex_c4': 'Ex. C4',
    'C4': 'C4',
    'd': 'D',
    'ex_d': 'Ex. D',
    'D': 'D',
}


## Inkorporer ti i hotspot scriptt
hotspot_legends = {
    'sum': 'Sum without D',
    'SumNew': 'Sum without D',
    'sum_d': 'Sum without D',
    'sumD': 'Sum without D',
    'a1-3': 'A1-3 Product',
    'A1-3': 'A1-3 Product',
    'A1to3': 'A1-3 Product',
    'a4': 'A4 Transport',
    'A4': 'A4 Transport',
    'a5': 'A5 Construction Site',
    'A5': 'A5 Construction Site',
    'b4': 'B4 Replacements',
    'B4': 'B4 Replacements',
    'c3': 'C3 Waste Treatment',
    'ex_c3': 'Existing C3 Waste treatment',
    'C3': 'C3 Waste Treatment',
    'c4': 'C4 Disposal',
    'ex_c4': 'Existing C4 Disposal',
    'C4': 'C4 Disposal',
    'd': 'D Outside project',
    'ex_d': 'Existing D Outside projekt',
    'D': 'D Outside project'
}
# Prøv denne metode af til at definere farve i stedet for at cycle igennem
# er tallet det index i farve-loopet som der anvendes??
hotspot_color_index = {
    'sum': 0,
    'SumNew': 0,
    'sum_d': 1,
    'sumD': 1,
    'a1-3': 0,
    'A1to3': 0,
    'A1-3': 0,
    'a4': 1,
    'A4': 1,
    'a5': 2,
    'A5': 2,
    'b4': 3,
    'B4': 3,
    'b6': 4,
    'B6': 4,
    'c3': 5,
    'ex_c3': 5,
    'C3': 5,
    'c4': 6,
    'ex_c4': 6,
    'C4': 6,
    'd': 9,
    'ex_d': 9,
    'D': 9,
    'ExC3': 5,
    'ExC4': 6,
    'ExD': 9,
}

# Tilføjet specialkursus januar - Terese
comp_elect_heat_title = {
    'total': 'Operation total, #'
}

comp_elect_heat_y_axis_labels = {
    'indicators': '#'
}

## Filtre de fra der anvendes
comp_elect_heat_legends = {
    'sum': 'Sum without D',
    'SumNew': 'Sum without D',
    'sum_d': 'Sum without D',
    'sumD': 'Sum without D',
    'a1-3': 'A1-3 Product',
    'A1-3': 'A1-3 Product',
    'A1to3': 'A1-3 Product',
    'a4': 'A4 Transport',
    'A4': 'A4 Transport',
    'a5': 'A5 Construction Site',
    'A5': 'A5 Construction Site',
    'b4': 'B4 Replacements',
    'B4': 'B4 Replacements',
    'c3': 'C3 Waste Treatment',
    'ex_c3': 'Existing C3 Waste treatment',
    'C3': 'C3 Waste Treatment',
    'c4': 'C4 Disposal',
    'ex_c4': 'Existing C4 Disposal',
    'C4': 'C4 Disposal',
    'd': 'D Outside project',
    'ex_d': 'Existing D Outside projekt',
    'D': 'D Outside project'
}


configuration_default_labels = {
    'conf_0': 'Conf. 0',
    'conf_1': 'Conf. 1',
    'conf_2': 'Conf. 2',
    'conf_3': 'Conf. 0',
    'conf_4': 'Conf. 1',
    'conf_5': 'Conf. 2',
}
