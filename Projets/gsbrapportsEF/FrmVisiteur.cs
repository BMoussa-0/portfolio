﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.Json;
using System.IO;


namespace gsbrapportsEF
{
    public partial class FrmVisiteur : Form
    {

        private gsbrapportsEntities mesDonneesEF;
        public FrmVisiteur(gsbrapportsEntities mesDonneesEF)
        {
            InitializeComponent();
            this.mesDonneesEF = mesDonneesEF;
            this.bdgsVisiteur.DataSource = mesDonneesEF.visiteurs.ToList();
        }

        private void FrmVisiteur_Load(object sender, EventArgs e)
        {
            
        }
        public static string login(visiteur visiteur)
        {
            char p = visiteur.prenom[0];
            string n = visiteur.nom;
            return p + n;
        }

        public static string mdp()
        {
            Random mdp = new Random();
            string fin = "";
            int chiffre = 0;
            for (int i = 0; i < 4; i++)
            {
                int p = mdp.Next(97, 122);
                char s = Convert.ToChar(p);
                fin += s;
            }
            
            for (int i = 0; i <= 1; i++)
            {
                int p = mdp.Next(1, 9);
                chiffre += p;
            }
            return fin + chiffre; 
        }
        private string getIdVisiteur()
        {
            var reqDernier = (from v in this.mesDonneesEF.visiteurs
                              orderby v.id descending
                              select v);
            visiteur dernierVisiteur = reqDernier.First();
            string n = dernierVisiteur.id;
            return n;
        }
        public visiteur newVisiteur()
        {
            visiteur newVisiteur = new visiteur();
            newVisiteur.id = txtId.Text;
            newVisiteur.nom = txtNom.Text;
            newVisiteur.prenom = txtPrenom.Text;
            newVisiteur.adresse = txtAdresse.Text;
            newVisiteur.cp = txtCP.Text;
            newVisiteur.ville = txtVille.Text;
            newVisiteur.dateEmbauche = dtEmbauche.Value;
            newVisiteur.login = login(newVisiteur).ToLower();
            newVisiteur.mdp = mdp();
            return newVisiteur;
        }
        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void tsbEnregistrer_Click(object sender, EventArgs e)
        {
            this.bdgsVisiteur.EndEdit();
            try
            {
                this.mesDonneesEF.visiteurs.Add(newVisiteur());
                this.mesDonneesEF.SaveChanges();
                MessageBox.Show("Enregistrement Validé");
            }
            catch (Exception ex)
            { 
                MessageBox.Show($"Erreur lors de l'enregistrement : {ex.Message}");
            }
        }

        private void bindingNavigatorDeleteItem_Click(object sender, EventArgs e)
        {
            using (var context = new gsbrapportsEntities())
            {
                    try
                    {
                        var idAsupprimer = txtId.Text;
                        var rapport = context.rapports.FirstOrDefault(r => r.idVisiteur == idAsupprimer);

                        if (rapport != null)
                        {
                            MessageBox.Show("Rapport existant pour ce visiteur !");
                        }
                        else 
                        {
                            var entiteAsupprimer = context.visiteurs.FirstOrDefault(v => v.id == idAsupprimer);

                            if (entiteAsupprimer == null)
                            {
                                MessageBox.Show("Visiteur introuvable.");
                                return;
                            }
                            context.visiteurs.Remove(entiteAsupprimer);
                            context.SaveChanges();
                            bdgsVisiteur.RemoveCurrent();
                            MessageBox.Show("Enregistrement supprimé.");
                        }
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Erreur lors de la suppression : {ex.Message}");
                    }
            }
        }

        private void bindingNavigatorAddNewItem_Click(object sender, EventArgs e)
        {
            this.txtId.Text = this.getIdVisiteur();
        }

        private void tsbModifier_Click(object sender, EventArgs e)
        {   
            this.bdgsVisiteur.EndEdit();
            try
            {
                this.mesDonneesEF.SaveChanges();
                MessageBox.Show("Modification Validé");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la modification : {ex.Message}");
            }
        }

        public List<string> reqRapport(string visiteurId)
        {
            var req = (from r in this.mesDonneesEF.rapports
                       where r.idVisiteur == visiteurId
                       select r.bilan).ToList();

            return req;
        }
        public void sauve(List<string> sc, string file)
        {
            string jsonString = JsonSerializer.Serialize(sc, new JsonSerializerOptions
            {
                WriteIndented = true
            });
            File.WriteAllText(file, jsonString);
        }

        private void btnExporter_Click(object sender, EventArgs e)
        {
            string idVisiteur = txtId.Text;
            var bilan = (from r in this.mesDonneesEF.rapports
                         where r.idVisiteur == idVisiteur
                         select r.bilan).ToList();
            try
            {
                this.sauve(bilan, $"Rapport_Du_Visiteur_{idVisiteur}.json");
                MessageBox.Show("Exportation réussie");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de l'exportation : {ex.Message}");
            }
        }

        private void txtId_TextChanged(object sender, EventArgs e)
        {

        }
    }
}