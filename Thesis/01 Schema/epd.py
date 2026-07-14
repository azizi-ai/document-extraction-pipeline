from pydantic import BaseModel, Field
from typing import Optional, List

class EPD(BaseModel):
    """
    Extraktionsschema für Umweltproduktdeklarationen (EPDs)
    """

    # Allgemeine Informationen
    herausgeber:            Optional[str] = None
    deklarationsinhaber:    Optional[str] = None
    deklarationsnummer:     Optional[str] = None
    deklariertes_produkt:   Optional[str] = None
    deklarierte_einheit:    Optional[str] = None
    gueltigkeitsdatum:      Optional[str] = None
    nutzungsdauer:          Optional[float] = None

    #TEC1.3
    rohdichte:              Optional[float] = None
    waermeleitfähigkeit:    Optional[float] = None
    waermekapazität:        Optional[float] = None

    # ENV1.1 Biogener Kohlenstoffgehalt
    # Einheit: kg C
    biogener_kohlestoffgehalt_im_produkt:    Optional[float] = None
    biogener_kohlestoffgehalt_in_verpackung: Optional[float] = None

    # Zertifizierungen (z.B. FSC, PEFC, CE, natureplus, ...)
    holzzertifizierungen: Optional[List[str]] = None

    # Brandklasse gem. EN 13501-1 (z.B. "A1", "B-s1,d0", "E")
    baustoffklasse:         Optional[str] = None
    brennendes_abtropfen:   Optional[str] = None
    rauchgasentwicklung:    Optional[str] = None

    svhc_vorhanden: Optional[bool] = None

    # ENV1.1 - Ökobilanz

    # GWP-total (Summe fossil + biogen + luluc)
    # Einheit kg CO2-Äq.
    gwp_t_global_warming_potential_total_a1:    Optional[float] = None
    gwp_t_global_warming_potential_total_a2:    Optional[float] = None
    gwp_t_global_warming_potential_total_a3:    Optional[float] = None
    gwp_t_global_warming_potential_total_a1_a3: Optional[float] = None
    gwp_t_global_warming_potential_total_a4:    Optional[float] = None
    gwp_t_global_warming_potential_total_a5:    Optional[float] = None
    gwp_t_global_warming_potential_total_b4:    Optional[float] = None
    gwp_t_global_warming_potential_total_b5:    Optional[float] = None
    gwp_t_global_warming_potential_total_b6:    Optional[float] = None
    gwp_t_global_warming_potential_total_c3:    Optional[float] = None
    gwp_t_global_warming_potential_total_c4:    Optional[float] = None
    gwp_t_global_warming_potential_total_d:     Optional[float] = None


    # GWP-fossil
    # Einheit kg CO2-Äq.
    gwp_f_global_warming_potential_fossil_fuels_a1:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_a2:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_a3:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_a1_a3:  Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_a4:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_a5:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_b4:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_b5:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_b6:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_c3:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_c4:     Optional[float] = None
    gwp_f_global_warming_potential_fossil_fuels_d:      Optional[float] = None


    # GWP-biogen
    # Einheit kg CO2-Äq.
    gwp_b_global_warming_potential_biogenic_a1:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_a2:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_a3:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_a1_a3:  Optional[float] = None
    gwp_b_global_warming_potential_biogenic_a4:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_a5:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_b4:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_b5:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_b6:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_c3:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_c4:     Optional[float] = None
    gwp_b_global_warming_potential_biogenic_d:      Optional[float] = None

    # GWP-luluc (Land Use and Land Use Change)
    # Einheit kg CO2-Äq.
    gwp_l_global_warming_potential_luluc_a1:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_a2:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_a3:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_a1_a3: Optional[float] = None
    gwp_l_global_warming_potential_luluc_a4:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_a5:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_b4:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_b5:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_b6:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_c3:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_c4:    Optional[float] = None
    gwp_l_global_warming_potential_luluc_d:     Optional[float] = None

    # Abbaupotenzial der stratosphärischen Ozonschicht (ODP)
    # Einheit: kg CFC 11-Äq.
    odp_depletion_potential_stratospheric_ozone_layer_a1:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_a2:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_a3:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_a1_a3:    Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_a4:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_a5:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_b4:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_b5:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_b6:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_c3:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_c4:       Optional[float] = None
    odp_depletion_potential_stratospheric_ozone_layer_d:        Optional[float] = None


    # Versauerungspotenzial (AP)
    # Einheit: mol H⁺-Äq.
    ap_acidification_potential_a1:      Optional[float] = None
    ap_acidification_potential_a2:      Optional[float] = None
    ap_acidification_potential_a3:      Optional[float] = None
    ap_acidification_potential_a1_a3:   Optional[float] = None
    ap_acidification_potential_a4:      Optional[float] = None
    ap_acidification_potential_a5:      Optional[float] = None
    ap_acidification_potential_b4:      Optional[float] = None
    ap_acidification_potential_b5:      Optional[float] = None
    ap_acidification_potential_b6:      Optional[float] = None
    ap_acidification_potential_c3:      Optional[float] = None
    ap_acidification_potential_c4:      Optional[float] = None
    ap_acidification_potential_d:       Optional[float] = None

    # Eutrophierungspotenzial Süßwasser (EP-freshwater)
    # Einheit: kg P-Äq.
    ep_fw_eutrophication_potential_freshwater_a1:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_a2:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_a3:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_a1_a3:    Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_a4:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_a5:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_b4:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_b5:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_b6:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_c3:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_c4:       Optional[float] = None
    ep_fw_eutrophication_potential_freshwater_d:        Optional[float] = None

    # Eutrophierungspotenzial Salzwasser (EP-marine)    
    # Einheit: mol N-Äq.
    ep_m_eutrophication_potential_marine_a1:       Optional[float] = None
    ep_m_eutrophication_potential_marine_a2:       Optional[float] = None
    ep_m_eutrophication_potential_marine_a3:       Optional[float] = None
    ep_m_eutrophication_potential_marine_a1_a3:    Optional[float] = None
    ep_m_eutrophication_potential_marine_a4:       Optional[float] = None
    ep_m_eutrophication_potential_marine_a5:       Optional[float] = None
    ep_m_eutrophication_potential_marine_b4:       Optional[float] = None
    ep_m_eutrophication_potential_marine_b5:       Optional[float] = None
    ep_m_eutrophication_potential_marine_b6:       Optional[float] = None
    ep_m_eutrophication_potential_marine_c3:       Optional[float] = None
    ep_m_eutrophication_potential_marine_c4:       Optional[float] = None
    ep_m_eutrophication_potential_marine_d:        Optional[float] = None


    # Eutrophierungspotenzial terrestrisch (EP-terrestrial)
    # Einheit: mol N-Äq.
    ep_t_eutrophication_potential_terrestrial_a1:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_a2:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_a3:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_a1_a3:  Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_a4:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_a5:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_b4:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_b5:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_b6:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_c3:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_c4:     Optional[float] = None
    ep_t_eutrophication_potential_terrestrial_d:      Optional[float] = None

    # POCP (Formation potential of tropospheric ozone)
    # Einheit: kg NMVOC-Äq.
    pocp_formation_potential_tropospheric_ozone_a1:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_a2:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_a3:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_a1_a3:  Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_a4:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_a5:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_b4:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_b5:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_b6:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_c3:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_c4:     Optional[float] = None
    pocp_formation_potential_tropospheric_ozone_d:      Optional[float] = None

    # ADPE - Potenzial für die Verknappung abiotischer Ressourcen – nicht fossil
    # Einheit: kg Sb-Äq.
    adpe_abiotic_depletion_potential_non_fossil_a1:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_a2:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_a3:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_a1_a3:  Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_a4:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_a5:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_b4:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_b5:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_b6:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_c3:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_c4:     Optional[float] = None
    adpe_abiotic_depletion_potential_non_fossil_d:      Optional[float] = None

    # ADPF (Abiotic depletion potential for fossil resources)
    # Einheit: MJ
    adpf_abiotic_depletion_potential_fossil_a1:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_a2:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_a3:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_a1_a3:  Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_a4:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_a5:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_b4:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_b5:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_b6:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_c3:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_c4:     Optional[float] = None
    adpf_abiotic_depletion_potential_fossil_d:      Optional[float] = None

    # PERT (Total use of renewable primary energy resources)
    # Einheit: MJ
    pert_total_use_renewable_primary_energy_a1:     Optional[float] = None
    pert_total_use_renewable_primary_energy_a2:     Optional[float] = None
    pert_total_use_renewable_primary_energy_a3:     Optional[float] = None
    pert_total_use_renewable_primary_energy_a1_a3:  Optional[float] = None
    pert_total_use_renewable_primary_energy_a4:     Optional[float] = None
    pert_total_use_renewable_primary_energy_a5:     Optional[float] = None
    pert_total_use_renewable_primary_energy_b4:     Optional[float] = None
    pert_total_use_renewable_primary_energy_b5:     Optional[float] = None
    pert_total_use_renewable_primary_energy_b6:     Optional[float] = None
    pert_total_use_renewable_primary_energy_c3:     Optional[float] = None
    pert_total_use_renewable_primary_energy_c4:     Optional[float] = None
    pert_total_use_renewable_primary_energy_d:      Optional[float] = None

    # PENRT (Total use of non-renewable primary energy resources)
    # Einheit: MJ
    penrt_total_use_non_renewable_primary_energy_a1:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_a2:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_a3:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_a1_a3: Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_a4:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_a5:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_b4:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_b5:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_b6:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_c3:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_c4:    Optional[float] = None
    penrt_total_use_non_renewable_primary_energy_d:     Optional[float] = None

    # FW (Use of net fresh water)
    # Einheit: m³
    fw_use_of_net_fresh_water_a1:       Optional[float] = None
    fw_use_of_net_fresh_water_a2:       Optional[float] = None
    fw_use_of_net_fresh_water_a3:       Optional[float] = None
    fw_use_of_net_fresh_water_a1_a3:    Optional[float] = None
    fw_use_of_net_fresh_water_a4:       Optional[float] = None
    fw_use_of_net_fresh_water_a5:       Optional[float] = None
    fw_use_of_net_fresh_water_b4:       Optional[float] = None
    fw_use_of_net_fresh_water_b5:       Optional[float] = None
    fw_use_of_net_fresh_water_b6:       Optional[float] = None
    fw_use_of_net_fresh_water_c3:       Optional[float] = None
    fw_use_of_net_fresh_water_c4:       Optional[float] = None
    fw_use_of_net_fresh_water_d:        Optional[float] = None

    # ENV 1.2 - Umweltrisiken

    # HWD - Gefährliche Abfälle zur Beseitigung (Hazardous Waste Disposed)
    # Einheit: kg
    hwd_hazardous_waste_disposed_a1:        Optional[float] = None
    hwd_hazardous_waste_disposed_a2:        Optional[float] = None
    hwd_hazardous_waste_disposed_a3:        Optional[float] = None
    hwd_hazardous_waste_disposed_a1_a3:     Optional[float] = None
    hwd_hazardous_waste_disposed_a4:        Optional[float] = None
    hwd_hazardous_waste_disposed_a5:        Optional[float] = None
    hwd_hazardous_waste_disposed_b4:        Optional[float] = None
    hwd_hazardous_waste_disposed_b5:        Optional[float] = None
    hwd_hazardous_waste_disposed_b6:        Optional[float] = None
    hwd_hazardous_waste_disposed_c3:        Optional[float] = None
    hwd_hazardous_waste_disposed_c4:        Optional[float] = None
    hwd_hazardous_waste_disposed_d:         Optional[float] = None

    # NHWD - Nicht gefährliche Abfälle zur Beseitigung (Non-Hazardous Waste Disposed)
    # Einheit: kg
    nhwd_non_hazardous_waste_disposed_a1:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_a2:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_a3:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_a1_a3:    Optional[float] = None
    nhwd_non_hazardous_waste_disposed_a4:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_a5:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_b4:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_b5:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_b6:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_c3:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_c4:       Optional[float] = None
    nhwd_non_hazardous_waste_disposed_d:        Optional[float] = None

    # RWD - Radioaktive Abfälle zur Beseitigung (Radioactive Waste Disposed)
    # Einheit: kg
    rwd_radioactive_waste_disposed_a1:      Optional[float] = None
    rwd_radioactive_waste_disposed_a2:      Optional[float] = None
    rwd_radioactive_waste_disposed_a3:      Optional[float] = None
    rwd_radioactive_waste_disposed_a1_a3:   Optional[float] = None
    rwd_radioactive_waste_disposed_a4:      Optional[float] = None
    rwd_radioactive_waste_disposed_a5:      Optional[float] = None
    rwd_radioactive_waste_disposed_b4:      Optional[float] = None
    rwd_radioactive_waste_disposed_b5:      Optional[float] = None
    rwd_radioactive_waste_disposed_b6:      Optional[float] = None
    rwd_radioactive_waste_disposed_c3:      Optional[float] = None
    rwd_radioactive_waste_disposed_c4:      Optional[float] = None
    rwd_radioactive_waste_disposed_d:       Optional[float] = None

    # TEC1.6 – Zirkuläres Bauen

    # CRU - Komponenten für die Wiederverwendung (Components for Reuse)
    # Einheit: kg
    cru_components_for_reuse_a1:        Optional[float] = None
    cru_components_for_reuse_a2:        Optional[float] = None
    cru_components_for_reuse_a3:        Optional[float] = None
    cru_components_for_reuse_a1_a3:     Optional[float] = None
    cru_components_for_reuse_a4:        Optional[float] = None
    cru_components_for_reuse_a5:        Optional[float] = None
    cru_components_for_reuse_b4:        Optional[float] = None
    cru_components_for_reuse_b5:        Optional[float] = None
    cru_components_for_reuse_b6:        Optional[float] = None
    cru_components_for_reuse_c3:        Optional[float] = None
    cru_components_for_reuse_c4:        Optional[float] = None
    cru_components_for_reuse_d:         Optional[float] = None

    # MFR - Stoffe zum Recycling (Materials for Recycling)
    # Einheit: kg
    mfr_materials_for_recycling_a1:     Optional[float] = None
    mfr_materials_for_recycling_a2:     Optional[float] = None
    mfr_materials_for_recycling_a3:     Optional[float] = None
    mfr_materials_for_recycling_a1_a3:  Optional[float] = None
    mfr_materials_for_recycling_a4:     Optional[float] = None
    mfr_materials_for_recycling_a5:     Optional[float] = None
    mfr_materials_for_recycling_b4:     Optional[float] = None
    mfr_materials_for_recycling_b5:     Optional[float] = None
    mfr_materials_for_recycling_b6:     Optional[float] = None
    mfr_materials_for_recycling_c3:     Optional[float] = None
    mfr_materials_for_recycling_c4:     Optional[float] = None
    mfr_materials_for_recycling_d:      Optional[float] = None

    # MER - Stoffe für die Energierückgewinnung (Materials for Energy Recovery)
    # Einheit: kg
    mer_materials_for_energy_recovery_a1:       Optional[float] = None
    mer_materials_for_energy_recovery_a2:       Optional[float] = None
    mer_materials_for_energy_recovery_a3:       Optional[float] = None
    mer_materials_for_energy_recovery_a1_a3:    Optional[float] = None
    mer_materials_for_energy_recovery_a4:       Optional[float] = None
    mer_materials_for_energy_recovery_a5:       Optional[float] = None
    mer_materials_for_energy_recovery_b4:       Optional[float] = None
    mer_materials_for_energy_recovery_b5:       Optional[float] = None
    mer_materials_for_energy_recovery_b6:       Optional[float] = None
    mer_materials_for_energy_recovery_c3:       Optional[float] = None
    mer_materials_for_energy_recovery_c4:       Optional[float] = None
    mer_materials_for_energy_recovery_d:        Optional[float] = None
