<!-- Division pour le sommaire -->
<nav class="menuLeft">
    <ul class="menu-ul">

        <li class="menu-item">
            Comptable :<br>
            <?php echo $_SESSION['prenom'] . "  " . $_SESSION['nom'] ?>
        </li>
        
        <li class="menu-item">
            <a href="index.php?uc=cumul&action=afficherFormulaire" title="Suivi du cumul">Cumul</a>
        </li>

        <li class="menu-item">
            <a href="index.php?uc=connexion&action=deconnexion" title="Se déconnecter">Déconnexion</a>
        </li>

        <li class="menu-item"><a href="index.php">Retour</a></li>

    </ul>
</nav>
<section class="content">