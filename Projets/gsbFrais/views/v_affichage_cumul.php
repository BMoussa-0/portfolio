<h2>Cumul des frais pour le mois : <?php echo($moisAnnee) ?></h2>

<table border="1">
    <thead>
        <tr>
            <th>Type de frais</th>
            <th>Cumul</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Kilometres</td>
            <td><?php echo($KM) ?></td>
        </tr>
        <tr>
            <td>Etape</td>
            <td><?php echo($ETP) ?></td>
        </tr>
        <tr>
            <td>Repas midi</td>
            <td><?php echo($REP) ?></td>
        </tr>
        <tr>
            <td>Nuitée</td>
            <td><?php echo($NUI) ?></td>
        </tr>

        <!-- Ajout de de la colonne Frais d'habillage où on retrouve la variable $HAB du controller c_cumul.php -->
        <tr>
            <td>Frais d'habillage</td>
            <td><?php echo($HAB) ?></td>
        </tr>
    </tbody>
</table>

