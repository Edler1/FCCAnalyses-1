
#ifndef  JETCLUSTERINGUTILS_ANALYZERS_H
#define  JETCLUSTERINGUTILS_ANALYZERS_H

#include <vector>
#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "fastjet/JetDefinition.hh"
#include "TRandom3.h"
#include "TMath.h"

/** Jet clustering utilities interface.
This represents a set functions and utilities to perfom jet clustering from a list of.
*/
namespace FCCAnalyses{

namespace JetClusteringUtils{

  /** @name JetClusteringUtils
   *  Jet clustering interface utilities.
  */
  ///@{

  const int Nmax_dmerge = 10;  // maximum number of d_{n, n+1} that are kept in FCCAnalysesJet


  struct flav_details{
    ROOT::VecOps::RVec<int> parton_flavour;
    ROOT::VecOps::RVec<int> hadron_flavour;
    ROOT::VecOps::RVec<fastjet::PseudoJet> ghost_pseudojets;
    std::vector<std::vector<int>> ghost_jetconstituents;
    ROOT::VecOps::RVec<int> ghostStatus;
    ROOT::VecOps::RVec<int> MCindex;
  };



  /** Structure to keep useful informations for the jets*/
  struct FCCAnalysesJet{
    TString clustering_algo;
    ROOT::VecOps::RVec<float> clustering_params;
    ROOT::VecOps::RVec<fastjet::PseudoJet> jets;
    std::vector<std::vector<int>> constituents;
    std::vector<float> exclusive_dmerge;   // vector of Nmax_dmerge  values associated with merging from n + 1 to n jets, for n =1, 2, ... 10
    std::vector<float> exclusive_dmerge_max ;
    ROOT::VecOps::RVec<int> flavour;
    //flav_details *flavour_details;
    flav_details flavour_details;
  };

  /** Set fastjet pseudoJet for later reconstruction*/
  std::vector<fastjet::PseudoJet> set_pseudoJets(const ROOT::VecOps::RVec<float> &px,
                                                 const ROOT::VecOps::RVec<float> &py,
                                                 const ROOT::VecOps::RVec<float> &pz,
                                                 const ROOT::VecOps::RVec<float> &e);

  /** Set fastjet pseudoJet for later reconstruction using px, py, pz and m
   *
   * This version is to be preferred over the px,py,pz,E version when m is known
   * accurately, because it uses double precision to reconstruct the energy,
   * reducing the size of rounding errors on FastJet calculations (e.g. of
   * PseudoJet masses)
   *
  */
  std::vector<fastjet::PseudoJet> set_pseudoJets_xyzm(const ROOT::VecOps::RVec<float> &px,
                                                      const ROOT::VecOps::RVec<float> &py,
                                                      const ROOT::VecOps::RVec<float> &pz,
                                                      const ROOT::VecOps::RVec<float> &m);

  /** Get fastjet pseudoJet after reconstruction from FCCAnalyses jets*/
  ROOT::VecOps::RVec<fastjet::PseudoJet> get_pseudoJets(const FCCAnalysesJet &in);

  /** Get fastjet constituents after reconstruction from FCCAnalyses jets*/
  std::vector<std::vector<int>> get_constituents(const FCCAnalysesJet &in);


  /// return the dmin corresponding to the recombination that went from n+1 to n jets
  float get_exclusive_dmerge(const FCCAnalysesJet &in, int n);

  float get_exclusive_dmerge_max(const FCCAnalysesJet &in, int n);

  /** Get jet px. Details. */
  ROOT::VecOps::RVec<float> get_px(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet py. Details. */
  ROOT::VecOps::RVec<float> get_py(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet pz. Details. */
  ROOT::VecOps::RVec<float> get_pz(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet energy. Details. */
  ROOT::VecOps::RVec<float> get_e(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet pt. Details. */
  ROOT::VecOps::RVec<float> get_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet p. Details. */
  ROOT::VecOps::RVec<float> get_p(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet mass. Details. */
  ROOT::VecOps::RVec<float> get_m(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet eta. Details. */
  ROOT::VecOps::RVec<float> get_eta(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet phi. Details. */
  ROOT::VecOps::RVec<float> get_phi(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet theta. Details. */
  ROOT::VecOps::RVec<float> get_theta(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);


  /// --- From Edi --- ///

  /** Reshape the given variable (given as a flat vector for the event) into 2d vector per jet. */
  std::vector<std::vector<float>> reshape2jet(ROOT::VecOps::RVec<float> var, std::vector<std::vector<int>> constituents);
  std::vector<std::vector<int>> int_2d();
  std::vector<std::vector<float>> float_2d(std::vector<std::vector<int>> constituents);

  /** Get number of constituents per jet. */
  ROOT::VecOps::RVec<float> get_nConstituents(std::vector<std::vector<int>> in);

  //The below fncs take already the reshaped values as arguments... Different from above...  
  /** Get difference of jet theta and jet constituent theta. */
  std::vector<std::vector<float>> get_dTheta(ROOT::VecOps::RVec<float> jet_theta, std::vector<std::vector<float>> constituents_theta);

  /** Get difference of jet phi and jet constituent phi in [-pi, pi]. */
  std::vector<std::vector<float>> get_dPhi(ROOT::VecOps::RVec<float> jet_phi, std::vector<std::vector<float>> constituents_phi);
  
  /** Get difference dR in theta-phi space of jet and jet constituent. */
  std::vector<std::vector<float>> get_dR(std::vector<std::vector<float>> constituents_dTheta, std::vector<std::vector<float>> constituents_dPhi);
  
  /** Get ratio of jet constituent |p| and jet |p|. */
  std::vector<std::vector<float>> get_pRel(ROOT::VecOps::RVec<float> jet_p, std::vector<std::vector<float>> constituents_p);

  /** Get ratio of jet constituent e and jet e. */
  std::vector<std::vector<float>> get_eRel(ROOT::VecOps::RVec<float> jet_e, std::vector<std::vector<float>> constituents_e);
  
  /** Get angles of jet constituents and jet axis. */
  std::vector<std::vector<float>> get_dAngle(ROOT::VecOps::RVec<float> jet_px, 
                                             ROOT::VecOps::RVec<float> jet_py, 
                                             ROOT::VecOps::RVec<float> jet_pz, 
                                             std::vector<std::vector<float>> constituents_px,
                                             std::vector<std::vector<float>> constituents_py,
                                             std::vector<std::vector<float>> constituents_pz
                                             );
  std::vector<float> get_angularity(float kappa, float beta, ROOT::VecOps::RVec<float> jet_e, std::vector<std::vector<float>> constituents_e, std::vector<std::vector<float>> constituents_dAngle);
  
  //int get_nJets(std::vector<std::vector<int>> constituents);


  /// ---          --- ///

  ///Internal methods
  //FCCAnalysesJet initialise_FCCAnalysesJet();
  FCCAnalysesJet initialise_FCCAnalysesJet(TString clustering_algo="default_string", ROOT::VecOps::RVec<float> clustering_params={});

  //FCCAnalysesJet build_FCCAnalysesJet(const std::vector<fastjet::PseudoJet> &in,
  //                                    const std::vector<float> &dmerge,
  //                                    const std::vector<float> &dmerge_max);

  FCCAnalysesJet build_FCCAnalysesJet(const std::vector<fastjet::PseudoJet> &in,
                                      const std::vector<float> &dmerge,
                                      const std::vector<float> &dmerge_max,
                                      TString clustering_algo="default_string",
                                      ROOT::VecOps::RVec<float> clustering_params={});



  std::vector<fastjet::PseudoJet> build_jets(fastjet::ClusterSequence & cs,
                                             int exclusive, float cut,
                                             int sorted);

  bool check(unsigned int n,
             int exclusive,
             float cut);

  fastjet::RecombinationScheme recomb_scheme(int recombination);

  std::vector<float> exclusive_dmerge(fastjet::ClusterSequence & cs,
                                      int do_dmarge_max)  ;


  ///@}

}//end NS JetClusteringUtils

}//end NS FCCAnalyses

#endif
