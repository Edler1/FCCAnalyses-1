#Mandatory: List of processes
processList = {
    # 1M b & c, 3M uds
    #'p8_ee_Zbb_ecm91':{'fraction':0.001, 'chunks':10}, #Run 0.1% statistics in two files named <outputDir>/p8_ee_Zbb_ecm91/chunk<N>.root
    #'p8_ee_Zcc_ecm91':{'fraction':0.001, 'chunks':10}, #Run 0.1% statistics in two files named <outputDir>/p8_ee_Zcc_ecm91/chunk<N>.root
    #'p8_ee_Zuds_ecm91':{'fraction':0.003, 'chunks':30}, #Run 0.3% statistics in one output file named <outputDir>/p8_ee_Zuds_ecm91.root

    # 400K b & c, 1M uds
    #'p8_ee_Zbb_ecm91':{'fraction':0.0004, 'chunks':4},
    #'p8_ee_Zcc_ecm91':{'fraction':0.0004, 'chunks':4},
    #'p8_ee_Zuds_ecm91':{'fraction':0.001, 'chunks':10},
    ##'p8_ee_Zuds_ecm91':{'fraction':0.0003, 'chunks':3},
    ##'p8_ee_Zcc_ecm91':{'fraction':0.0001, 'chunks':1},
    'p8_ee_Zbb_ecm91':{'fraction':0.0001, 'chunks':1},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/"
#outputDir   = "/afs/cern.ch/work/k/kgautam/private/latest/FCCAnalyses/outputs/FCCee/KG/"

#Optional: ncpus, default is 4
nCPUS       = 8

#Optional running on HTCondor, default is False
#runBatch    = True

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"
#batchQueue = "espresso"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df

            # alias
            .Alias("Particle0", "Particle#0.index") 
            .Alias("Particle1", "Particle#1.index") 
            .Alias("Jet3","Jet#3.index")
            .Alias("Muon0","Muon#0.index")
            .Alias("Electron0","Electron#0.index")
            .Alias("Photon0","Photon#0.index")
            .Alias("MCRecoAssociations0","MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1","MCRecoAssociations#1.index")
            .Define("Particle1_indices", "Particle1")

            # Reco'd particles
            .Define("RP_px",        "ReconstructedParticle::get_px(ReconstructedParticles)")
            .Define("RP_py",        "ReconstructedParticle::get_py(ReconstructedParticles)")
            .Define("RP_pz",        "ReconstructedParticle::get_pz(ReconstructedParticles)")               
            .Define("RP_m",         "ReconstructedParticle::get_mass(ReconstructedParticles)")
            .Define("RP_charge",    "ReconstructedParticle::get_charge(ReconstructedParticles)")
            #Even neutrals have tracks now?
            #.Define("RP_hasTRK",    "ReconstructedParticle2Track::hasTRK(ReconstructedParticles)")
            .Define("RP_hasTRK",    "ROOT::VecOps::RVec<int> result; for (auto& charge : RP_charge){if(std::abs(charge)>0) result.push_back(1); else result.push_back(0);}return result;")
            .Define("RP_charged",   "ReconstructedParticle::sel_tag(1)(RP_hasTRK, ReconstructedParticles)")
            .Define("RP_neutral",   "ReconstructedParticle::sel_tag(0)(RP_hasTRK, ReconstructedParticles)")
            .Define("RP_isMuon",    "ReconstructedParticle::is_particle(Muon0, ReconstructedParticles)")
            .Define("RP_isElectron","ReconstructedParticle::is_particle(Electron0, ReconstructedParticles)")
            .Define("RP_isPhoton",  "ReconstructedParticle::is_particle(Photon0, ReconstructedParticles)")
            
            .Define("RP_PID",          "ReconstructedParticle::get_PID(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
            ##.Define("RP_charged_PID",   "ReconstructedParticle::sel_template(true)(RP_hasTRK, RP_PID)")
            .Define("is_S",          "ReconstructedParticle::is_S(RP_PID)")
            .Define("is_Kaon",          "ReconstructedParticle::is_Kaon(RP_PID)")
            .Define("is_Kaon_smearedUniform080",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.80, 0.10)")
            .Define("is_Kaon_smearedUniform090",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.90, 0.10)")
            .Define("is_Kaon_smearedUniform095",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.95, 0.10)")
            .Define("is_Kaon_smearedUniform060",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.60, 0.10)")
            .Define("is_Kaon_smearedUniform040",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.40, 0.10)")
            .Define("is_Kaon_smearedUniform020",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.20, 0.10)")
            .Define("is_Kaon_smearedUniform000",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 0.00, 0.00)")
            .Define("is_Kaon_smearedUniform100",          "ReconstructedParticle::is_Kaon_smearedUniform(RP_PID, 1.00, 0.00)")
            #.Define("is_Kaon_smearedUniform010",          "ReconstructedParticle::is_Kaon_smearedUniform010(RP_PID)")
            #.Define("is_Kaon_smearedUniform005",          "ReconstructedParticle::is_Kaon_smearedUniform005(RP_PID)")
            #.Define("is_Kaon_smearedUniform001",          "ReconstructedParticle::is_Kaon_smearedUniform001(RP_PID)")

            #Get charged PF vars 
            .Define("RP_charged_charge",    "ReconstructedParticle::get_charge(RP_charged)")
            .Define("RP_charged_p",         "ReconstructedParticle::get_p(RP_charged)")
            #.Define("RP_charged_p_template","ReconstructedParticle::get_p(RP_template)")
            .Define("RP_charged_theta",     "ReconstructedParticle::get_theta(RP_charged)")
            .Define("RP_charged_phi",       "ReconstructedParticle::get_phi(RP_charged)")
            .Define("RP_charged_mass",      "ReconstructedParticle::get_mass(RP_charged)") #should think about this, do we really mean mass of RP or assuming pion?
            .Define("RP_charged_Z0",        "ReconstructedParticle2Track::getRP2TRK_Z0(RP_charged, EFlowTrack_1)")
            .Define("RP_charged_D0",        "ReconstructedParticle2Track::getRP2TRK_D0(RP_charged, EFlowTrack_1)")
            .Define("RP_charged_Z0_sig",    "ReconstructedParticle2Track::getRP2TRK_Z0_sig(RP_charged, EFlowTrack_1)")
            .Define("RP_charged_D0_sig",    "ReconstructedParticle2Track::getRP2TRK_D0_sig(RP_charged, EFlowTrack_1)")

            ####Get neutral PF vars 
            .Define("RP_neutral_p", "ReconstructedParticle::get_p(RP_neutral)")

            # First, reconstruct a vertex from all tracks
            .Define("VertexObject_allTracks",  "VertexFitterSimple::VertexFitter_Tk ( 1, EFlowTrack_1, true, 4.5, 20e-3, 300)")
            # Select the tracks that are reconstructed  as primaries
            .Define("RecoedPrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( VertexObject_allTracks, EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0., 0)")
            .Define("n_RecoedPrimaryTracks",  "ReconstructedParticle2Track::getTK_n( RecoedPrimaryTracks )")
            # the final primary vertex : 
            .Define("PV", "VertexFitterSimple::VertexFitter_Tk ( 1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300) ") # primary vertex object
            .Define("PrimaryVertex", "VertexingUtils::get_VertexData( PV )")
            
            # the secondary tracks
            .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1,  RecoedPrimaryTracks )")
            .Define("n_SecondaryTracks", "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )
            
            # which of the tracks are primary according to the reco algprithm
            .Define("IsPrimary_based_on_reco",  "VertexFitterSimple::IsPrimary_forTracks( EFlowTrack_1,  RecoedPrimaryTracks )")
            
            # jet clustering (ee-kt) before reconstructing SVs in event
            # build psedo-jets with the Reconstructed final particles
            .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
            # run jet clustering with all reco particles. ee_kt_algorithm, exclusive clustering, exactly 2 jets, E-scheme
            .Define("FCCAnalysesJets_ee_kt", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
            # get the jets out of the structure
            .Define("jets_ee_kt", "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_kt)")
            # get the jet constituents out of the structure
            .Define("jetconstituents", "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_kt)")
            #find SVs in jets
            .Define("SV_jet", "VertexFinderLCFIPlus::get_SV_jets(ReconstructedParticles, EFlowTrack_1, PV, IsPrimary_based_on_reco, jets_ee_kt, jetconstituents)")
            #find V0s in jets
            .Define("V0", "VertexFinderLCFIPlus::get_V0s_jet(ReconstructedParticles, EFlowTrack_1, IsPrimary_based_on_reco, jets_ee_kt, jetconstituents, PV)")
            #separate by jetsh. none of this will be needed once get_V0_jet is of the form Rvec<RVec<V0>>
            .Define("V0_jet", "VertexingUtils::get_svInJets(V0.vtx, V0.nSV_jet)")
            #separate tracks by jets
            .Define("Tracks", "VertexingUtils::get_tracksInJets(ReconstructedParticles, EFlowTrack_1, jets_ee_kt, jetconstituents)")


            ###############
            #Some hacky reshaping of the constis 
            .Define("RPj_hasTRK",     "JetClusteringUtils::reshape2jet(RP_hasTRK, jetconstituents)")
            #.Define("split_indices", "ReconstructedParticle::index_splitter(ReconstructedParticles, RP_hasTRK)")
            .Define("split_indices",  "ReconstructedParticle::index_splitter(RP_hasTRK)")
            .Define("split_jetconstituents", "ReconstructedParticle::index_converter(jetconstituents, split_indices)")
            .Define("charged_constis","ReconstructedParticle::sel_template(true)(RPj_hasTRK, split_jetconstituents)")
            .Define("neutral_constis","ReconstructedParticle::sel_template(false)(RPj_hasTRK, split_jetconstituents)")
            
            #Some hacky reshaping of the event level RP ids
            .Define("RPj_isMuon",     "JetClusteringUtils::reshape2jet(RP_isMuon, jetconstituents)")
            .Define("RPj_isElectron", "JetClusteringUtils::reshape2jet(RP_isElectron, jetconstituents)")
            .Define("RPj_isPhoton",   "JetClusteringUtils::reshape2jet(RP_isPhoton, jetconstituents)")
            .Define("RPj_PID", "JetClusteringUtils::reshape2jet(RP_PID, jetconstituents)")
            .Define("RPj_is_S", "JetClusteringUtils::reshape2jet(is_S, jetconstituents)")
            .Define("RPj_is_Kaon", "JetClusteringUtils::reshape2jet(is_Kaon, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform080", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform080, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform090", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform090, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform095", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform095, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform060", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform060, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform040", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform040, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform020", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform020, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform000", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform000, jetconstituents)")
            .Define("RPj_is_Kaon_smearedUniform100", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform100, jetconstituents)")
            #.Define("RPj_is_Kaon_smearedUniform010", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform010, jetconstituents)")
            #.Define("RPj_is_Kaon_smearedUniform005", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform005, jetconstituents)")
            #.Define("RPj_is_Kaon_smearedUniform001", "JetClusteringUtils::reshape2jet(is_Kaon_smearedUniform001, jetconstituents)")
                
            
            #Get jet-level vars
            .Define("jets_nRP_charged","JetClusteringUtils::get_nConstituents(charged_constis)")
            .Define("jets_nRP_neutral","JetClusteringUtils::get_nConstituents(neutral_constis)")
            .Define("jets_p",          "JetClusteringUtils::get_p(jets_ee_kt)")
            .Define("jets_px",         "JetClusteringUtils::get_px(jets_ee_kt)")
            .Define("jets_py",         "JetClusteringUtils::get_py(jets_ee_kt)")
            .Define("jets_pz",         "JetClusteringUtils::get_pz(jets_ee_kt)")
            .Define("jets_theta",      "JetClusteringUtils::get_theta(jets_ee_kt)")
            .Define("jets_phi",        "JetClusteringUtils::get_phi(jets_ee_kt)")
            .Define("jets_m",          "JetClusteringUtils::get_m(jets_ee_kt)")
            .Define("jets_e",          "JetClusteringUtils::get_e(jets_ee_kt)")

            #.Define("n_jets",          "JetClusteringUtils::get_n_jets(jets_ee_kt)")
            .Define("n_jets",          "jets_ee_kt.size()")
            
            .Define("jets_pt",         "JetClusteringUtils::get_pt(jets_ee_kt)")
            .Define("jets_eta",        "JetClusteringUtils::get_eta(jets_ee_kt)")
            





            .Define("jets_flavour",    "JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            .Define("jets_flavour_unmatched",    "JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            .Define("jets_ghostFlavour", "JetTaggingUtils::get_flavour(Particle, Particle1, FCCAnalysesJets_ee_kt, pseudo_jets)")
            .Define("jets_ghostFlavour_angle03status70", "JetTaggingUtils::get_flavour(Particle, Particle1, FCCAnalysesJets_ee_kt, pseudo_jets, 0.3, 70)")            
            .Define("jets_ghostFlavour_angle03status20", "JetTaggingUtils::get_flavour(Particle, Particle1, FCCAnalysesJets_ee_kt, pseudo_jets, 0.3, 20)")            
            #.Define("jets_flavour", "ROOT::VecOps::RVec<float> abs_flav; for(auto& flav : jets_ghostFlavour){if(flav==21){abs_flav.push_back(0); continue;};abs_flav.push_back(std::abs(flav));}; return abs_flav")    
            .Define("H_flavour", "JetTaggingUtils::get_H_flavour(jets_ee_kt, Particle, Particle1)")
            .Redefine("jets_flavour", "ROOT::VecOps::RVec<float> flav; for(int i=0; i<jets_flavour.size(); ++i){if(jets_flavour.at(i)==H_flavour.at(i)) flav.push_back(jets_flavour.at(i)); else flav.push_back(0);}return flav;")

            #.Define("jets_flavour",    "JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")

            #.Define("jets_flavour_placeholder","JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            .Define("jets_onehot", "ReconstructedParticle::one_hot_encode_Higgs(jets_flavour)")
            .Define("jets_isGbar", "jets_onehot[0]")
            .Define("jets_isBbar", "jets_onehot[1]")
            .Define("jets_isCbar", "jets_onehot[2]")
            .Define("jets_isSbar", "jets_onehot[3]")
            .Define("jets_isUbar", "jets_onehot[4]")
            .Define("jets_isDbar", "jets_onehot[5]")
            .Define("jets_isD",    "jets_onehot[7]")
            .Define("jets_isU",    "jets_onehot[8]")
            .Define("jets_isS",    "jets_onehot[9]")
            .Define("jets_isC",    "jets_onehot[10]")
            .Define("jets_isB",    "jets_onehot[11]")
            .Define("jets_isG",    "jets_onehot[12]")
            .Define("jets_isUndefined","jets_onehot[6]")

            #Aliasing to match Alexandre's files
            .Define("isU", "std::vector<int> isU; for(int i=0; i<jets_isU.size(); ++i){isU.push_back(jets_isU[i]+jets_isUbar[i]);}; return isU;")
            .Define("isD", "std::vector<int> isD; for(int i=0; i<jets_isD.size(); ++i){isD.push_back(jets_isD[i]+jets_isDbar[i]);}; return isD;")
            .Define("isS", "std::vector<int> isS; for(int i=0; i<jets_isS.size(); ++i){isS.push_back(jets_isS[i]+jets_isSbar[i]);}; return isS;")
            .Define("isC", "std::vector<int> isC; for(int i=0; i<jets_isC.size(); ++i){isC.push_back(jets_isC[i]+jets_isCbar[i]);}; return isC;")
            .Define("isB", "std::vector<int> isB; for(int i=0; i<jets_isB.size(); ++i){isB.push_back(jets_isB[i]+jets_isBbar[i]);}; return isB;")
            .Define("isG", "std::vector<int> isG; for(int i=0; i<jets_isG.size(); ++i){isG.push_back(jets_isG[i]+jets_isGbar[i]);}; return isG;")
            .Define("isUndefined", "std::vector<int> isUndefined(jets_isUndefined.begin(), jets_isUndefined.end()); return isUndefined;")


            #Ghost Flavour 
            .Redefine("jets_ghostFlavour", "ROOT::VecOps::RVec<float> flav; for(int i=0; i<jets_ghostFlavour.size(); ++i){if(jets_ghostFlavour.at(i)==H_flavour.at(i)) flav.push_back(jets_ghostFlavour.at(i)); else flav.push_back(0);}return flav;")
            .Define("jets_onehot_ghost", "ReconstructedParticle::one_hot_encode_Higgs(jets_ghostFlavour)")
            .Define("jets_isGbar_ghost", "jets_onehot_ghost[0]")
            .Define("jets_isBbar_ghost", "jets_onehot_ghost[1]")
            .Define("jets_isCbar_ghost", "jets_onehot_ghost[2]")
            .Define("jets_isSbar_ghost", "jets_onehot_ghost[3]")
            .Define("jets_isUbar_ghost", "jets_onehot_ghost[4]")
            .Define("jets_isDbar_ghost", "jets_onehot_ghost[5]")
            .Define("jets_isD_ghost",    "jets_onehot_ghost[7]")
            .Define("jets_isU_ghost",    "jets_onehot_ghost[8]")
            .Define("jets_isS_ghost",    "jets_onehot_ghost[9]")
            .Define("jets_isC_ghost",    "jets_onehot_ghost[10]")
            .Define("jets_isB_ghost",    "jets_onehot_ghost[11]")
            .Define("jets_isG_ghost",    "jets_onehot_ghost[12]")
            .Define("jets_isUndefined_ghost","jets_onehot_ghost[6]")

            #Aliasing to match Alexandre's files
            .Define("isU_ghost", "std::vector<int> isU_ghost; for(int i=0; i<jets_isU_ghost.size(); ++i){isU_ghost.push_back(jets_isU_ghost[i]+jets_isUbar_ghost[i]);}; return isU_ghost;")
            .Define("isD_ghost", "std::vector<int> isD_ghost; for(int i=0; i<jets_isD_ghost.size(); ++i){isD_ghost.push_back(jets_isD_ghost[i]+jets_isDbar_ghost[i]);}; return isD_ghost;")
            .Define("isS_ghost", "std::vector<int> isS_ghost; for(int i=0; i<jets_isS_ghost.size(); ++i){isS_ghost.push_back(jets_isS_ghost[i]+jets_isSbar_ghost[i]);}; return isS_ghost;")
            .Define("isC_ghost", "std::vector<int> isC_ghost; for(int i=0; i<jets_isC_ghost.size(); ++i){isC_ghost.push_back(jets_isC_ghost[i]+jets_isCbar_ghost[i]);}; return isC_ghost;")
            .Define("isB_ghost", "std::vector<int> isB_ghost; for(int i=0; i<jets_isB_ghost.size(); ++i){isB_ghost.push_back(jets_isB_ghost[i]+jets_isBbar_ghost[i]);}; return isB_ghost;")
            .Define("isG_ghost", "std::vector<int> isG_ghost; for(int i=0; i<jets_isG_ghost.size(); ++i){isG_ghost.push_back(jets_isG_ghost[i]+jets_isGbar_ghost[i]);}; return isG_ghost;")
            .Define("isUndefined_ghost", "std::vector<int> isUndefined_ghost(jets_isUndefined_ghost.begin(), jets_isUndefined_ghost.end()); return isUndefined_ghost;")
            




            #H_flavour
            #.Define("jets_flavour_placeholder","JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            .Define("jets_onehot_H", "ReconstructedParticle::one_hot_encode_Higgs(H_flavour)")
            .Define("jets_isGbar_H", "jets_onehot_H[0]")
            .Define("jets_isBbar_H", "jets_onehot_H[1]")
            .Define("jets_isCbar_H", "jets_onehot_H[2]")
            .Define("jets_isSbar_H", "jets_onehot_H[3]")
            .Define("jets_isUbar_H", "jets_onehot_H[4]")
            .Define("jets_isDbar_H", "jets_onehot_H[5]")
            .Define("jets_isD_H",    "jets_onehot_H[7]")
            .Define("jets_isU_H",    "jets_onehot_H[8]")
            .Define("jets_isS_H",    "jets_onehot_H[9]")
            .Define("jets_isC_H",    "jets_onehot_H[10]")
            .Define("jets_isB_H",    "jets_onehot_H[11]")
            .Define("jets_isG_H",    "jets_onehot_H[12]")
            .Define("jets_isUndefined_H","jets_onehot_H[6]")

            #Aliasing to match Alexandre's files
            .Define("isU_H", "std::vector<int> isU_H; for(int i=0; i<jets_isU_H.size(); ++i){isU_H.push_back(jets_isU_H[i]+jets_isUbar_H[i]);}; return isU_H;")
            .Define("isD_H", "std::vector<int> isD_H; for(int i=0; i<jets_isD_H.size(); ++i){isD_H.push_back(jets_isD_H[i]+jets_isDbar_H[i]);}; return isD_H;")
            .Define("isS_H", "std::vector<int> isS_H; for(int i=0; i<jets_isS_H.size(); ++i){isS_H.push_back(jets_isS_H[i]+jets_isSbar_H[i]);}; return isS_H;")
            .Define("isC_H", "std::vector<int> isC_H; for(int i=0; i<jets_isC_H.size(); ++i){isC_H.push_back(jets_isC_H[i]+jets_isCbar_H[i]);}; return isC_H;")
            .Define("isB_H", "std::vector<int> isB_H; for(int i=0; i<jets_isB_H.size(); ++i){isB_H.push_back(jets_isB_H[i]+jets_isBbar_H[i]);}; return isB_H;")
            .Define("isG_H", "std::vector<int> isG_H; for(int i=0; i<jets_isG_H.size(); ++i){isG_H.push_back(jets_isG_H[i]+jets_isGbar_H[i]);}; return isG_H;")
            .Define("isUndefined_H", "std::vector<int> isUndefined_H(jets_isUndefined_H.begin(), jets_isUndefined_H.end()); return isUndefined_H;")




            #Ghost Flavour w/ angle=0.3 and partonStatus=70s
            .Redefine("jets_ghostFlavour_angle03status70", "ROOT::VecOps::RVec<float> flav; for(int i=0; i<jets_ghostFlavour_angle03status70.size(); ++i){if(jets_ghostFlavour_angle03status70.at(i)==H_flavour.at(i)) flav.push_back(jets_ghostFlavour_angle03status70.at(i)); else flav.push_back(0);}return flav;")
            #.Define("jets_flavour_placeholder","JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            .Define("jets_onehot_ghost_angle03status70", "ReconstructedParticle::one_hot_encode_Higgs(jets_ghostFlavour_angle03status70)")
            .Define("jets_isGbar_ghost_angle03status70", "jets_onehot_ghost_angle03status70[0]")
            .Define("jets_isBbar_ghost_angle03status70", "jets_onehot_ghost_angle03status70[1]")
            .Define("jets_isCbar_ghost_angle03status70", "jets_onehot_ghost_angle03status70[2]")
            .Define("jets_isSbar_ghost_angle03status70", "jets_onehot_ghost_angle03status70[3]")
            .Define("jets_isUbar_ghost_angle03status70", "jets_onehot_ghost_angle03status70[4]")
            .Define("jets_isDbar_ghost_angle03status70", "jets_onehot_ghost_angle03status70[5]")
            .Define("jets_isD_ghost_angle03status70",    "jets_onehot_ghost_angle03status70[7]")
            .Define("jets_isU_ghost_angle03status70",    "jets_onehot_ghost_angle03status70[8]")
            .Define("jets_isS_ghost_angle03status70",    "jets_onehot_ghost_angle03status70[9]")
            .Define("jets_isC_ghost_angle03status70",    "jets_onehot_ghost_angle03status70[10]")
            .Define("jets_isB_ghost_angle03status70",    "jets_onehot_ghost_angle03status70[11]")
            .Define("jets_isG_ghost_angle03status70",    "jets_onehot_ghost_angle03status70[12]")
            .Define("jets_isUndefined_ghost_angle03status70","jets_onehot_ghost_angle03status70[6]")

            #Aliasing to match Alexandre's files
            .Define("isU_ghost_angle03status70", "std::vector<int> isU_ghost_angle03status70; for(int i=0; i<jets_isU_ghost_angle03status70.size(); ++i){isU_ghost_angle03status70.push_back(jets_isU_ghost_angle03status70[i]+jets_isUbar_ghost_angle03status70[i]);}; return isU_ghost_angle03status70;")
            .Define("isD_ghost_angle03status70", "std::vector<int> isD_ghost_angle03status70; for(int i=0; i<jets_isD_ghost_angle03status70.size(); ++i){isD_ghost_angle03status70.push_back(jets_isD_ghost_angle03status70[i]+jets_isDbar_ghost_angle03status70[i]);}; return isD_ghost_angle03status70;")
            .Define("isS_ghost_angle03status70", "std::vector<int> isS_ghost_angle03status70; for(int i=0; i<jets_isS_ghost_angle03status70.size(); ++i){isS_ghost_angle03status70.push_back(jets_isS_ghost_angle03status70[i]+jets_isSbar_ghost_angle03status70[i]);}; return isS_ghost_angle03status70;")
            .Define("isC_ghost_angle03status70", "std::vector<int> isC_ghost_angle03status70; for(int i=0; i<jets_isC_ghost_angle03status70.size(); ++i){isC_ghost_angle03status70.push_back(jets_isC_ghost_angle03status70[i]+jets_isCbar_ghost_angle03status70[i]);}; return isC_ghost_angle03status70;")
            .Define("isB_ghost_angle03status70", "std::vector<int> isB_ghost_angle03status70; for(int i=0; i<jets_isB_ghost_angle03status70.size(); ++i){isB_ghost_angle03status70.push_back(jets_isB_ghost_angle03status70[i]+jets_isBbar_ghost_angle03status70[i]);}; return isB_ghost_angle03status70;")
            .Define("isG_ghost_angle03status70", "std::vector<int> isG_ghost_angle03status70; for(int i=0; i<jets_isG_ghost_angle03status70.size(); ++i){isG_ghost_angle03status70.push_back(jets_isG_ghost_angle03status70[i]+jets_isGbar_ghost_angle03status70[i]);}; return isG_ghost_angle03status70;")
            .Define("isUndefined_ghost_angle03status70", "std::vector<int> isUndefined_ghost_angle03status70(jets_isUndefined_ghost_angle03status70.begin(), jets_isUndefined_ghost_angle03status70.end()); return isUndefined_ghost_angle03status70;")



            #Ghost Flavour w/ angle=0.3 and partonStatus=20s
            .Redefine("jets_ghostFlavour_angle03status20", "ROOT::VecOps::RVec<float> flav; for(int i=0; i<jets_ghostFlavour_angle03status20.size(); ++i){if(jets_ghostFlavour_angle03status20.at(i)==H_flavour.at(i)) flav.push_back(jets_ghostFlavour_angle03status20.at(i)); else flav.push_back(0);}return flav;")
            #.Define("jets_flavour_placeholder","JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            .Define("jets_onehot_ghost_angle03status20", "ReconstructedParticle::one_hot_encode_Higgs(jets_ghostFlavour_angle03status20)")
            .Define("jets_isGbar_ghost_angle03status20", "jets_onehot_ghost_angle03status20[0]")
            .Define("jets_isBbar_ghost_angle03status20", "jets_onehot_ghost_angle03status20[1]")
            .Define("jets_isCbar_ghost_angle03status20", "jets_onehot_ghost_angle03status20[2]")
            .Define("jets_isSbar_ghost_angle03status20", "jets_onehot_ghost_angle03status20[3]")
            .Define("jets_isUbar_ghost_angle03status20", "jets_onehot_ghost_angle03status20[4]")
            .Define("jets_isDbar_ghost_angle03status20", "jets_onehot_ghost_angle03status20[5]")
            .Define("jets_isD_ghost_angle03status20",    "jets_onehot_ghost_angle03status20[7]")
            .Define("jets_isU_ghost_angle03status20",    "jets_onehot_ghost_angle03status20[8]")
            .Define("jets_isS_ghost_angle03status20",    "jets_onehot_ghost_angle03status20[9]")
            .Define("jets_isC_ghost_angle03status20",    "jets_onehot_ghost_angle03status20[10]")
            .Define("jets_isB_ghost_angle03status20",    "jets_onehot_ghost_angle03status20[11]")
            .Define("jets_isG_ghost_angle03status20",    "jets_onehot_ghost_angle03status20[12]")
            .Define("jets_isUndefined_ghost_angle03status20","jets_onehot_ghost_angle03status20[6]")

            #Aliasing to match Alexandre's files
            .Define("isU_ghost_angle03status20", "std::vector<int> isU_ghost_angle03status20; for(int i=0; i<jets_isU_ghost_angle03status20.size(); ++i){isU_ghost_angle03status20.push_back(jets_isU_ghost_angle03status20[i]+jets_isUbar_ghost_angle03status20[i]);}; return isU_ghost_angle03status20;")
            .Define("isD_ghost_angle03status20", "std::vector<int> isD_ghost_angle03status20; for(int i=0; i<jets_isD_ghost_angle03status20.size(); ++i){isD_ghost_angle03status20.push_back(jets_isD_ghost_angle03status20[i]+jets_isDbar_ghost_angle03status20[i]);}; return isD_ghost_angle03status20;")
            .Define("isS_ghost_angle03status20", "std::vector<int> isS_ghost_angle03status20; for(int i=0; i<jets_isS_ghost_angle03status20.size(); ++i){isS_ghost_angle03status20.push_back(jets_isS_ghost_angle03status20[i]+jets_isSbar_ghost_angle03status20[i]);}; return isS_ghost_angle03status20;")
            .Define("isC_ghost_angle03status20", "std::vector<int> isC_ghost_angle03status20; for(int i=0; i<jets_isC_ghost_angle03status20.size(); ++i){isC_ghost_angle03status20.push_back(jets_isC_ghost_angle03status20[i]+jets_isCbar_ghost_angle03status20[i]);}; return isC_ghost_angle03status20;")
            .Define("isB_ghost_angle03status20", "std::vector<int> isB_ghost_angle03status20; for(int i=0; i<jets_isB_ghost_angle03status20.size(); ++i){isB_ghost_angle03status20.push_back(jets_isB_ghost_angle03status20[i]+jets_isBbar_ghost_angle03status20[i]);}; return isB_ghost_angle03status20;")
            .Define("isG_ghost_angle03status20", "std::vector<int> isG_ghost_angle03status20; for(int i=0; i<jets_isG_ghost_angle03status20.size(); ++i){isG_ghost_angle03status20.push_back(jets_isG_ghost_angle03status20[i]+jets_isGbar_ghost_angle03status20[i]);}; return isG_ghost_angle03status20;")
            .Define("isUndefined_ghost_angle03status20", "std::vector<int> isUndefined_ghost_angle03status20(jets_isUndefined_ghost_angle03status20.begin(), jets_isUndefined_ghost_angle03status20.end()); return isUndefined_ghost_angle03status20;")

            
            #.Define("jets_isBbar_placeholder", "jets_onehot[0]")
            #.Define("jets_isCbar_placeholder", "jets_onehot[1]")
            #.Define("jets_isSbar_placeholder", "jets_onehot[2]")
            #.Define("jets_isUbar_placeholder", "jets_onehot[3]")
            #.Define("jets_isDbar_placeholder", "jets_onehot[4]")
            #.Define("jets_isD_placeholder",    "jets_onehot[6]")
            #.Define("jets_isU_placeholder",    "jets_onehot[7]")
            #.Define("jets_isS_placeholder",    "jets_onehot[8]")
            #.Define("jets_isC_placeholder",    "jets_onehot[9]")
            #.Define("jets_isB_placeholder",    "jets_onehot[10]")
            #.Define("jets_isUndefined_placeholder","jets_onehot[5]")
               
            #.Define("jets_isBbar",     "int jets_isBbar = jets_isBbar_placeholder[0]; return jets_isBbar;")
            #.Define("jets_isCbar",     "int jets_isCbar = jets_isCbar_placeholder[0]; return jets_isCbar;")
            #.Define("jets_isSbar",     "int jets_isSbar = jets_isSbar_placeholder[0]; return jets_isSbar;")
            #.Define("jets_isUbar",     "int jets_isUbar = jets_isUbar_placeholder[0]; return jets_isUbar;")
            #.Define("jets_isDbar",     "int jets_isDbar = jets_isDbar_placeholder[0]; return jets_isDbar;")
            #.Define("jets_isD",        "int jets_isD = jets_isD_placeholder[0]; return jets_isD;")
            #.Define("jets_isU",        "int jets_isU = jets_isU_placeholder[0]; return jets_isU;")
            #.Define("jets_isS",        "int jets_isS = jets_isS_placeholder[0]; return jets_isS;")
            #.Define("jets_isC",        "int jets_isC = jets_isC_placeholder[0]; return jets_isC;")
            #.Define("jets_isB",        "int jets_isB = jets_isB_placeholder[0]; return jets_isB;")
            #.Define("jets_isUndefined","int jets_isUndefined = jets_isUndefined_placeholder[0]; return jets_isUndefined;") #is this undefined or u+d?
            
            
            #.Define("jets_ee_kt_e",          "JetClusteringUtils::get_e(jets_ee_kt)")
            #.Define("jets_ee_kt_px",         "JetClusteringUtils::get_px(jets_ee_kt)")
            #.Define("jets_ee_kt_py",         "JetClusteringUtils::get_py(jets_ee_kt)")
            #.Define("jets_ee_kt_pz",         "JetClusteringUtils::get_pz(jets_ee_kt)")
            #.Define("jets_ee_kt_flavour",    "JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")
            #.Define("jets_ee_kt_flavour_anti","JetTaggingUtils::get_flavour_anti(jets_ee_kt, Particle)")
            #.Define("jets_theta_placeholder", "JetClusteringUtils::get_theta(jets_ee_kt)")
            #.Define("jets_phi_placeholder",   "JetClusteringUtils::get_phi(jets_ee_kt)")
            #.Define("jets_p_placeholder",     "JetClusteringUtils::get_p(jets_ee_kt)")


               
            #Reshape event-level charged RP to jet-level charged RP
            #.Define("int_2d",    "JetClusteringUtils::int_2d()")
            #.Define("float_2d",    "JetClusteringUtils::float_2d(charged_constis)")
            .Define("RPj_charged_p",    "JetClusteringUtils::reshape2jet(RP_charged_p, charged_constis)")
            .Define("RPj_charged_theta","JetClusteringUtils::reshape2jet(RP_charged_theta, charged_constis)")
            .Define("RPj_charged_phi",  "JetClusteringUtils::reshape2jet(RP_charged_phi, charged_constis)")
            
            #.Define("RPj_charged_theta_placeholder","JetClusteringUtils::reshape2jet(RP_charged_theta, charged_constis)")
            #.Define("RPj_charged_phi_placeholder",  "JetClusteringUtils::reshape2jet(RP_charged_phi, charged_constis)")
            #.Define("RPj_charged_p_placeholder",    "JetClusteringUtils::reshape2jet(RP_charged_p, charged_constis)")
            
            .Define("RPj_charged_mass",      "JetClusteringUtils::reshape2jet(RP_charged_mass, charged_constis)")
            .Define("RPj_charged_Z0",        "JetClusteringUtils::reshape2jet(RP_charged_Z0, charged_constis)")
            .Define("RPj_charged_D0",        "JetClusteringUtils::reshape2jet(RP_charged_D0, charged_constis)")
            .Define("RPj_charged_Z0_sig",    "JetClusteringUtils::reshape2jet(RP_charged_Z0_sig, charged_constis)")
            .Define("RPj_charged_D0_sig",    "JetClusteringUtils::reshape2jet(RP_charged_D0_sig, charged_constis)")
            .Define("RPj_charged_dTheta",    "JetClusteringUtils::get_dTheta(jets_theta, RPj_charged_theta)")
            .Define("RPj_charged_dPhi",      "JetClusteringUtils::get_dPhi(jets_phi, RPj_charged_phi)")
            .Define("RPj_charged_pRel",      "JetClusteringUtils::get_pRel(jets_p, RPj_charged_p)")
            .Define("RPj_charged_isMuon",    "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_isMuon)")
            .Define("RPj_charged_isElectron","ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_isElectron)")
            
            .Define("RPj_charged_PID", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_PID)")
            .Define("RPj_charged_is_S", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_S)")
            .Define("RPj_charged_is_Kaon", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon)")
            .Define("RPj_charged_is_Kaon_smearedUniform080", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform080)")
            .Define("RPj_charged_is_Kaon_smearedUniform090", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform090)")
            .Define("RPj_charged_is_Kaon_smearedUniform095", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform095)")
            .Define("RPj_charged_is_Kaon_smearedUniform060", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform060)")
            .Define("RPj_charged_is_Kaon_smearedUniform040", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform040)")
            .Define("RPj_charged_is_Kaon_smearedUniform020", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform020)")
            .Define("RPj_charged_is_Kaon_smearedUniform000", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform000)")
            .Define("RPj_charged_is_Kaon_smearedUniform100", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform100)")
            #.Define("RPj_charged_is_Kaon_smearedUniform010", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform010)")
            #.Define("RPj_charged_is_Kaon_smearedUniform005", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform005)")
            #.Define("RPj_charged_is_Kaon_smearedUniform001", "ReconstructedParticle::sel_template(true)(RPj_hasTRK, RPj_is_Kaon_smearedUniform001)")
            
               
            #Reshape event-level neutral RP to jet-level neutral RP
            .Define("RPj_neutral_p", "JetClusteringUtils::reshape2jet(RP_neutral_p, neutral_constis)")
               
            #.Define("RPj_neutral_p_placeholder", "JetClusteringUtils::reshape2jet(RP_neutral_p, neutral_constis)")
            
            .Define("RPj_neutral_pRel",     "JetClusteringUtils::get_pRel(jets_p, RPj_neutral_p)")
            .Define("RPj_neutral_isPhoton", "ReconstructedParticle::sel_template(false)(RPj_hasTRK, RPj_isPhoton)")
            
            #.Define("isB", "int isB = jets_isB_placeholder[0]; return isB;")
            #.Define("isC", "int isC = jets_isC_placeholder[0]; return isC;")
            #.Define("isUD", "int isUD = jets_isU_placeholder[0]+jets_isD_placeholder[0]; return isUD;")
            #.Define("isS", "int isS = jets_isS_placeholder[0]; return isS;")
            #.Define("isUndefined", "int isUndefined = 0; return isUndefined;")
            .Define("jet_pt",                   "JetClusteringUtils::get_pt(jets_ee_kt)")
            .Define("jet_eta",                  "JetClusteringUtils::get_eta(jets_ee_kt)")
            .Define("n_Cpfcand",                "std::vector<int> n_Cpfcand(jets_nRP_charged.begin(), jets_nRP_charged.end()); return n_Cpfcand;")
            #.Define("n_Cpfcand",                "int n_Cpfcand = jets_nRP_charged; return n_Cpfcand;")
            .Define("nCpfcand",                 "jets_nRP_charged;")
            .Define("n_Npfcand",                "std::vector<int> n_Npfcand(jets_nRP_neutral.begin(), jets_nRP_neutral.end()); return n_Npfcand;")
            #.Define("n_Npfcand",                "int n_Npfcand = jets_nRP_neutral); return n_Npfcand;")
            .Define("nNpfcand",                 "jets_nRP_neutral")

            #### what's going on? from here -
            ###.Define("Cpfcan_BtagPf_trackEtaRel","RPj_charged_p")
            ###.Define("Cpfcan_BtagPf_trackPtRel", "RPj_charged_theta")
            ###.Define("Cpfcan_BtagPf_trackDeltaR","RPj_charged_phi")
            ###.Define("Cpfcan_quality",           "RPj_charged_mass")
            ###.Define("Npfcan_ptrel",             "RPj_neutral_p")
            #### - to here
            ###.Define("Npfcan_isGamma",           "RPj_neutral_isPhoton")
            #.Define("isU",                      "int isU = jets_isU[0]; return isU;")
            #.Define("isD",                      "int isD = jets_isD[0]; return isD;")


            ##################



            
            # JET VARIABLES
            .Define("n_sv",       "VertexingUtils::get_n_SV_jets(SV_jet)") # no of SVs per jet
            #.Define("jet_p",      "JetClusteringUtils::get_p(jets_ee_kt)") # jet momentum
            #.Define("jet_pt",     "JetClusteringUtils::get_pt(jets_ee_kt)") # jet transverse momentum
            #.Define("jet_energy", "JetClusteringUtils::get_e(jets_ee_kt)") # jet energy
            #.Define("jet_mass",   "JetClusteringUtils::get_m(jets_ee_kt)") # jet mass
            #.Define("jet_theta",  "JetClusteringUtils::get_theta(jets_ee_kt)") # jet polar angle
            #.Define("jet_eta",    "JetClusteringUtils::get_eta(jets_ee_kt)") # jet pseudo-rapidity
            #.Define("jet_phi",    "JetClusteringUtils::get_phi(jets_ee_kt)") # jet azimuthal angle

            #SV VARIABLES
            #.Define("sv_mass1",   "myUtils::get_Vertex_mass(SV.vtx, ReconstructedParticles)") # SV mass (first way)
            .Define("sv_mass",    "VertexingUtils::get_invM(SV_jet)") # SV mass (second way)
            #.Define("sv_p4",      "VertexingUtils::get_p4_SV(SV_jet)") # SV momentum (4 vector)
            .Define("sv_p",       "VertexingUtils::get_pMag_SV(SV_jet)") # SV momentum (magnitude)
            .Define("sv_ntracks", "VertexingUtils::get_VertexNtrk(SV_jet)") # SV daughters (no of tracks)
            .Define("sv_chi2",    "VertexingUtils::get_chi2_SV(SV_jet)") # SV chi2 (not normalised)
            .Define("sv_normchi2","VertexingUtils::get_norm_chi2_SV(SV_jet)") # SV chi2 (normalised)
            .Define("sv_ndf",     "VertexingUtils::get_nDOF_SV(SV_jet)") # SV no of DOF
            .Define("sv_theta",   "VertexingUtils::get_theta_SV(SV_jet)") # SV polar angle (theta)
            .Define("sv_phi",     "VertexingUtils::get_phi_SV(SV_jet)") # SV azimuthal angle (phi)
            .Define("sv_thetarel","VertexingUtils::get_relTheta_SV(SV_jet, jets_ee_kt)") # SV polar angle wrt jet
            .Define("sv_phirel",  "VertexingUtils::get_relPhi_SV(SV_jet, jets_ee_kt)") # SV azimuthal angle wrt jet
            .Define("sv_costhetasvpv","VertexingUtils::get_pointingangle_SV(SV_jet, PV)") # SV pointing angle
            .Define("sv_dxy",     "VertexingUtils::get_dxy_SV(SV_jet, PV)") # SV distance from PV (in xy plane)
            .Define("sv_d3d",     "VertexingUtils::get_d3d_SV(SV_jet, PV)") # SV distance from PV (in 3D)

            #V0 VARIABLES
            .Define("v0_pid",     "VertexingUtils::get_pdg_V0(V0.pdgAbs, V0.nSV_jet)") # V0 pdg id
            .Define("v0_mass",    "VertexingUtils::get_invM_V0(V0.invM, V0.nSV_jet)") # V0 invariant mass
            #.Define("v0_p4",      "VertexingUtils::get_p4_SV(V0_jet)") # V0 momentum (4 vector)
            .Define("v0_p",       "VertexingUtils::get_pMag_SV(V0_jet)") # V0 momentum (magnitude)
            .Define("v0_ntracks", "VertexingUtils::get_VertexNtrk(V0_jet)") # V0 daughters (no of tracks)
            .Define("v0_chi2",    "VertexingUtils::get_chi2_SV(V0_jet)") # V0 chi2 (not normalised)
            .Define("v0_normchi2","VertexingUtils::get_norm_chi2_SV(V0_jet)") # V0 chi2 (normalised but same as above)
            .Define("v0_ndf",     "VertexingUtils::get_nDOF_SV(V0_jet)") # V0 no of DOF (always 1)
            .Define("v0_theta",   "VertexingUtils::get_theta_SV(V0_jet)") # V0 polar angle (theta)
            .Define("v0_phi",     "VertexingUtils::get_phi_SV(V0_jet)") # V0 azimuthal angle (phi)
            .Define("v0_thetarel","VertexingUtils::get_relTheta_SV(V0_jet, jets_ee_kt)") # V0 polar angle wrt jets
            .Define("v0_phirel",  "VertexingUtils::get_relPhi_SV(V0_jet, jets_ee_kt)") # V0 azimuthal angle wrt jets
            .Define("v0_costhetasvpv","VertexingUtils::get_pointingangle_SV(V0_jet, PV)") # V0 pointing angle
            .Define("v0_dxy",     "VertexingUtils::get_dxy_SV(V0_jet, PV)") # V0 distance from PV (in xy plane)
            .Define("v0_d3d",     "VertexingUtils::get_d3d_SV(V0_jet, PV)") # V0 distance from PV (in 3D)






            #### CHARGED PF CANDIDATE VARIABLES (TRACK)
            ####.Define("n_Cpfcan",   "ReconstructedParticle2Track::getTK_n(Tracks[0])") # no of tracks
            ####.Define("Cpfcan_dz",  "ReconstructedParticle2Track::getRP2TRK_Z0(ReconstructedParticles, Tracks[0])") # longitudinal IP
            ####.Define("Cpfcan_dxy", "ReconstructedParticle2Track::getRP2TRK_D0(ReconstructedParticles, Tracks[0])") # transverse IP
            ####.Define("Cpfcan_sdz", "ReconstructedParticle2Track::getRP2TRK_Z0_sig(ReconstructedParticles, Tracks[0])") # longitudinal IP significance
            ####.Define("Cpfcan_sdxy","ReconstructedParticle2Track::getRP2TRK_D0_sig(ReconstructedParticles, Tracks[0])") # transverse IP significance
            ####.Define("Cpfcan_phi", "ReconstructedParticle2Track::getRP2TRK_phi(ReconstructedParticles, Tracks[0])") # azimuthal angle
            ####.Define("Cpfcan_theta","ReconstructedParticle2Track::getRP2TRK_theta(ReconstructedParticles, Tracks[0])") # polar angle
            ####.Define("Cpfcan_p",   "ReconstructedParticle2Track::getRP2TRK_mom(ReconstructedParticles, Tracks[0])") # momentum magnitude
            ####.Define("Cpfcan_charge","ReconstructedParticle2Track::getRP2TRK_charge(ReconstructedParticles, Tracks[0])") # charge
           
            #.Define("RPj_charged_p_flattened",          "JetClusteringUtils::reshape2flat(RPj_charged_p)")
            #.Define("RPj_charged_Idx",          "JetClusteringUtils::jet_Idx(RPj_charged_p)")
            ##.Define("nJets",          "JetClusteringUtils::get_nJets(jetconstituents)")

            ##.Define("PID",          "ReconstructedParticle::get_PID(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
            ##.Define("is_S",          "ReconstructedParticle::is_S(PID)")
            ##.Define("is_Kaon",          "ReconstructedParticle::is_Kaon(PID)")
            ##.Define("is_Kaon_smearedUniform010",          "ReconstructedParticle::is_Kaon_smearedUniform010(PID)")
            ##.Define("is_Kaon_smearedUniform005",          "ReconstructedParticle::is_Kaon_smearedUniform005(PID)")
            ##.Define("is_Kaon_smearedUniform001",          "ReconstructedParticle::is_Kaon_smearedUniform001(PID)")
            
            #Redefinitions for consistency...
            .Redefine("H_flavour", "return std::vector<int>(H_flavour.begin(), H_flavour.end());")
            .Redefine("jets_p", "return std::vector<float>(jets_p.begin(), jets_p.end());")
            .Redefine("jets_px", "return std::vector<float>(jets_px.begin(), jets_px.end());")
            .Redefine("jets_py", "return std::vector<float>(jets_py.begin(), jets_py.end());")
            .Redefine("jets_pz", "return std::vector<float>(jets_pz.begin(), jets_pz.end());")
            .Redefine("jets_theta", "return std::vector<float>(jets_theta.begin(), jets_theta.end());")
            .Redefine("jets_phi", "return std::vector<float>(jets_phi.begin(), jets_phi.end());")
            .Redefine("jets_m", "return std::vector<float>(jets_m.begin(), jets_m.end());")
            .Redefine("jets_e", "return std::vector<float>(jets_e.begin(), jets_e.end());")
            .Redefine("jets_nRP_charged", "return std::vector<float>(jets_nRP_charged.begin(), jets_nRP_charged.end());")
            .Redefine("jets_nRP_neutral", "return std::vector<float>(jets_nRP_neutral.begin(), jets_nRP_neutral.end());")
            
            .Redefine("jets_pt", "return std::vector<float>(jets_pt.begin(), jets_pt.end());")
            .Redefine("jets_eta", "return std::vector<float>(jets_eta.begin(), jets_eta.end());")

            .Redefine("sv_mass", "std::vector<std::vector<float>> result; for(auto& sv_mass_single : sv_mass){std::vector<float> tmp_res(sv_mass_single.begin(), sv_mass_single.end()); result.push_back(tmp_res);} return result;")
            ####.Redefine("sv_p4", "std::vector<std::vector<float>> result; for(auto& sv_p4_single : sv_p4){std::vector<float> tmp_res(sv_p4_single.begin(), sv_p4_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_p", "std::vector<std::vector<float>> result; for(auto& sv_p_single : sv_p){std::vector<float> tmp_res(sv_p_single.begin(), sv_p_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_ntracks", "std::vector<std::vector<int>> result; for(auto& sv_ntracks_single : sv_ntracks){std::vector<int> tmp_res(sv_ntracks_single.begin(), sv_ntracks_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_chi2", "std::vector<std::vector<float>> result; for(auto& sv_chi2_single : sv_chi2){std::vector<float> tmp_res(sv_chi2_single.begin(), sv_chi2_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_normchi2", "std::vector<std::vector<float>> result; for(auto& sv_normchi2_single : sv_normchi2){std::vector<float> tmp_res(sv_normchi2_single.begin(), sv_normchi2_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_ndf", "std::vector<std::vector<int>> result; for(auto& sv_ndf_single : sv_ndf){std::vector<int> tmp_res(sv_ndf_single.begin(), sv_ndf_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_theta", "std::vector<std::vector<float>> result; for(auto& sv_theta_single : sv_theta){std::vector<float> tmp_res(sv_theta_single.begin(), sv_theta_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_phi", "std::vector<std::vector<float>> result; for(auto& sv_phi_single : sv_phi){std::vector<float> tmp_res(sv_phi_single.begin(), sv_phi_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_thetarel", "std::vector<std::vector<float>> result; for(auto& sv_thetarel_single : sv_thetarel){std::vector<float> tmp_res(sv_thetarel_single.begin(), sv_thetarel_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_phirel", "std::vector<std::vector<float>> result; for(auto& sv_phirel_single : sv_phirel){std::vector<float> tmp_res(sv_phirel_single.begin(), sv_phirel_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_costhetasvpv", "std::vector<std::vector<float>> result; for(auto& sv_costhetasvpv_single : sv_costhetasvpv){std::vector<float> tmp_res(sv_costhetasvpv_single.begin(), sv_costhetasvpv_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_dxy", "std::vector<std::vector<float>> result; for(auto& sv_dxy_single : sv_dxy){std::vector<float> tmp_res(sv_dxy_single.begin(), sv_dxy_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("sv_d3d", "std::vector<std::vector<float>> result; for(auto& sv_d3d_single : sv_d3d){std::vector<float> tmp_res(sv_d3d_single.begin(), sv_d3d_single.end()); result.push_back(tmp_res);} return result;")


            .Redefine("v0_pid", "std::vector<std::vector<float>> result; for(auto& v0_pid_single : v0_pid){std::vector<float> tmp_res(v0_pid_single.begin(), v0_pid_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_mass", "std::vector<std::vector<float>> result; for(auto& v0_mass_single : v0_mass){std::vector<float> tmp_res(v0_mass_single.begin(), v0_mass_single.end()); result.push_back(tmp_res);} return result;")
            #.Redefine("v0_p4", "std::vector<std::vector<float>> result; for(auto& v0_p4_single : v0_p4){std::vector<float> tmp_res(v0_p4_single.begin(), v0_p4_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_p", "std::vector<std::vector<float>> result; for(auto& v0_p_single : v0_p){std::vector<float> tmp_res(v0_p_single.begin(), v0_p_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_ntracks", "std::vector<std::vector<int>> result; for(auto& v0_ntracks_single : v0_ntracks){std::vector<int> tmp_res(v0_ntracks_single.begin(), v0_ntracks_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_chi2", "std::vector<std::vector<float>> result; for(auto& v0_chi2_single : v0_chi2){std::vector<float> tmp_res(v0_chi2_single.begin(), v0_chi2_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_normchi2", "std::vector<std::vector<float>> result; for(auto& v0_normchi2_single : v0_normchi2){std::vector<float> tmp_res(v0_normchi2_single.begin(), v0_normchi2_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_ndf", "std::vector<std::vector<int>> result; for(auto& v0_ndf_single : v0_ndf){std::vector<int> tmp_res(v0_ndf_single.begin(), v0_ndf_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_theta", "std::vector<std::vector<float>> result; for(auto& v0_theta_single : v0_theta){std::vector<float> tmp_res(v0_theta_single.begin(), v0_theta_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_phi", "std::vector<std::vector<float>> result; for(auto& v0_phi_single : v0_phi){std::vector<float> tmp_res(v0_phi_single.begin(), v0_phi_single.end()); result.push_back(tmp_res);} return result;")
            ###.Redefine("v0_thetarel", "std::vector<std::vector<float>> result; for(auto& v0_thetarel_single : v0_thetarel){std::vector<float> tmp_res(v0_thetarel_single.begin(), v0_thetarel_single.end()); result.push_back(tmp_res);} return result;")
            ###.Redefine("v0_phirel", "std::vector<std::vector<float>> result; for(auto& v0_phirel_single : v0_phirel){std::vector<float> tmp_res(v0_phirel_single.begin(), v0_phirel_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_costhetasvpv", "std::vector<std::vector<float>> result; for(auto& v0_costhetasvpv_single : v0_costhetasvpv){std::vector<float> tmp_res(v0_costhetasvpv_single.begin(), v0_costhetasvpv_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_dxy", "std::vector<std::vector<float>> result; for(auto& v0_dxy_single : v0_dxy){std::vector<float> tmp_res(v0_dxy_single.begin(), v0_dxy_single.end()); result.push_back(tmp_res);} return result;")
            .Redefine("v0_d3d", "std::vector<std::vector<float>> result; for(auto& v0_d3d_single : v0_d3d){std::vector<float> tmp_res(v0_d3d_single.begin(), v0_d3d_single.end()); result.push_back(tmp_res);} return result;")

 
            ##.Redefine("PID", "std::vector<std::vector<float>> result; for(auto& : PID_single : PID){std::vector<float> tmp_res(PID_single.begin(), PID_single.end()); result.push_back(tmp_res);} return result;")
            ##.Redefine("is_S", "std::vector<std::vector<float>> result; for(auto& : is_S_single : is_S){std::vector<float> tmp_res(is_S_single.begin(), is_S_single.end()); result.push_back(tmp_res);} return result;")
            ##.Redefine("is_Kaon", "std::vector<std::vector<float>> result; for(auto& : is_Kaon_single : is_Kaon){std::vector<float> tmp_res(is_Kaon_single.begin(), is_Kaon_single.end()); result.push_back(tmp_res);} return result;")
            ##.Redefine("is_Kaon_smearedUniform010", "std::vector<std::vector<float>> result; for(auto& : is_Kaon_smearedUniform010_single : is_Kaon_smearedUniform010){std::vector<float> tmp_res(is_Kaon_smearedUniform010_single.begin(), is_Kaon_smearedUniform010_single.end()); result.push_back(tmp_res);} return result;")
            ##.Redefine("is_Kaon_smearedUniform005", "std::vector<std::vector<float>> result; for(auto& : is_Kaon_smearedUniform005_single : is_Kaon_smearedUniform005){std::vector<float> tmp_res(is_Kaon_smearedUniform005_single.begin(), is_Kaon_smearedUniform005_single.end()); result.push_back(tmp_res);} return result;")
            ##.Redefine("is_Kaon_smearedUniform001", "std::vector<std::vector<float>> result; for(auto& : is_Kaon_smearedUniform001_single : is_Kaon_smearedUniform001){std::vector<float> tmp_res(is_Kaon_smearedUniform001_single.begin(), is_Kaon_smearedUniform001_single.end()); result.push_back(tmp_res);} return result;")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

            # Jet Flavour
            "isU",
            "isD",
            "isS",
            "isC",
            "isB",
            "isG",
            "isUndefined",
            "H_flavour",
            "isU_ghost",
            "isD_ghost",
            "isS_ghost",
            "isC_ghost",
            "isB_ghost",
            "isG_ghost",
            "isUndefined_ghost",
            "isU_H",
            "isD_H",
            "isS_H",
            "isC_H",
            "isB_H",
            "isG_H",
            "isUndefined_H",
            "isU_ghost_angle03status70",
            "isD_ghost_angle03status70",
            "isS_ghost_angle03status70",
            "isC_ghost_angle03status70",
            "isB_ghost_angle03status70",
            "isG_ghost_angle03status70",
            "isUndefined_ghost_angle03status70",
            "isU_ghost_angle03status20",
            "isD_ghost_angle03status20",
            "isS_ghost_angle03status20",
            "isC_ghost_angle03status20",
            "isB_ghost_angle03status20",
            "isG_ghost_angle03status20",
            "isUndefined_ghost_angle03status20",
            
            # Jet-level Variables
            "jets_p",
            "jets_px",
            "jets_py",
            "jets_pz",
            "jets_theta",
            "jets_phi",
            "jets_m",
            "jets_e",
            "jets_nRP_charged",
            "jets_nRP_neutral",
            
            "jets_pt",
            "jets_eta",
            
            # charged PF
            "RPj_charged_p",
            "RPj_charged_theta",
            "RPj_charged_phi",
            "RPj_charged_mass",
            "RPj_charged_Z0",
            "RPj_charged_D0",
            "RPj_charged_Z0_sig",
            "RPj_charged_D0_sig",
            "RPj_charged_dTheta",
            "RPj_charged_dPhi",
            "RPj_charged_pRel",
            "RPj_charged_isMuon",
            "RPj_charged_isElectron",
            
            # neutral PF
            "RPj_neutral_p",
            "RPj_neutral_pRel",
            "RPj_neutral_isPhoton",            

            #### jet variables
            ####"nSV",
            ####"jet_p",
            ####"jet_pt",
            ####"jet_energy",
            ####"jet_mass",
            ####"jet_theta",
            ####"jet_eta",
            ####"jet_phi",

            ##"jets_nRP_charged",
            ##"jets_nRP_neutral",

            #"n_jets",
            
            #"jets_pt",
            #"jets_eta",
            
            #"jets_isBbar",
            #"jets_isCbar",
            #"jets_isSbar",
            #"jets_isUbar",
            #"jets_isDbar",
            #"jets_isD",
            #"jets_isU",
            #"jets_isS",
            #"jets_isC",
            #"jets_isB",
            #"jets_isUndefined",

            ##"sv_mass",
            
            #"isB",
            #"isC",
            #"isUD",
            #"isS",
            #"isUndefined",
            #"jet_pt",
            #"jet_eta",
            #"n_Cpfcand",
            #"nCpfcand",
            #"Cpfcan_BtagPf_trackEtaRel",
            #"Cpfcan_BtagPf_trackPtRel",
            #"Cpfcan_BtagPf_trackDeltaR",
            #"Cpfcan_quality",
            #"n_Npfcand",
            #"nNpfcand",
            #"Npfcan_ptrel",
            #"Npfcan_isGamma",
            #"isU",
            #"isD",


            #SV variables
            ####"sv_mass1",
            ########"nSV",
            "sv_mass",
            ####"sv_p4",
            "sv_p",
            "sv_ntracks",
            "sv_chi2",
            "sv_normchi2",
            "sv_ndf",
            "sv_theta",
            "sv_phi",
            "sv_thetarel",
            "sv_phirel",
            "sv_costhetasvpv",
            "sv_dxy",
            "sv_d3d",

            #V0 variables
            ###"nV0",
            "v0_pid",
            "v0_mass",
            #"v0_p4",
            "v0_p",
            "v0_ntracks",
            "v0_chi2",
            "v0_normchi2",
            "v0_ndf",
            "v0_theta",
            "v0_phi",
            ###"v0_thetarel",
            ###"v0_phirel",
            "v0_costhetasvpv",
            "v0_dxy",
            "v0_d3d",

            #extra stuff
            #"nJets",
            "RPj_charged_PID",
            "RPj_charged_is_S",
            "RPj_charged_is_Kaon",
            "RPj_charged_is_Kaon_smearedUniform080",
            "RPj_charged_is_Kaon_smearedUniform090",
            "RPj_charged_is_Kaon_smearedUniform095",
            "RPj_charged_is_Kaon_smearedUniform060",
            "RPj_charged_is_Kaon_smearedUniform040",
            "RPj_charged_is_Kaon_smearedUniform020",
            "RPj_charged_is_Kaon_smearedUniform000",
            "RPj_charged_is_Kaon_smearedUniform100",



            ##### ENDS HERE CURRENTLY

            #### track variables
            ####"n_Cpfcan",
            ####"Cpfcan_dz",
            ####"Cpfcan_dxy",
            ####"Cpfcan_sdz",
            ####"Cpfcan_sdxy",
            ####"Cpfcan_phi",
            ####"Cpfcan_theta",
            ####"Cpfcan_p",
            ####"Cpfcan_charge"
        ]
        return branchList
