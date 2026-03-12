<!-- 
misurazioni.php 
Soluzione prova scritta Sistemi e reti
Sessione straordinaria Esame di Stato 2016 
ITT Informatica e Telecomunicazioni Articolazione Informatica"  -->
<!DOCTYPE html>
<?php
session_start();
?>
<html>
<head>
	<title>Misurazioni</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head> 
<style>
 body{font-size:130%} select{font-size:100%;width:400px}
 input[type=submit],[type=reset]{width:120px;font-size:100%}
 a{text-decoration:none}
 table, th, td {border: 1px solid black;}
</style>
<script language="javascript" type="text/javascript"> 
function validaForm(){
	var paziente=mioForm.paziente.value;
	if (paziente=="Seleziona"){
		alert("Seleziona il paziente");
		return false;
	}
	var d1=mioForm.data1.value;
	var d2=mioForm.data2.value;
	if(d1=="" || d2==""){
		alert("Selezionare le due date");
		return false;
	}
	if(d1>d2){
		alert("Selezionare correttamente le due date");
		return false;
	}
}
</script>
<?php
if (!isset($_POST["paziente"]))
  {	?>
  <body> 
	<form id="mioForm" method="post" onsubmit="return validaForm();">
    <?php 
	  $idmedico=$_SESSION["id"]; 
	 //quando il medico ha effettuato il login, è stata creata la variabile di sessione $_SESSION["id"]
	 // per testare il codice occorre creare e impostare questa variabile, ad esempio con lo script PHP:
	 // session_start();$_SESSION['id']=x  dove x è l'id del medico scelto per il test 
	  $conn=mysqli_connect("localhost","root","mypassword","iotmedici");
	  // query SQL per ottenere il nome e cognome del medico che ha eseguito il login
	  $s="Select nomecognome from medici where id=$idmedico";
	  $q=mysqli_query($conn,$s);
	  $r =mysqli_fetch_array($q);
	  echo "<h2>Dott. $r[0] <br/>Monitoraggio remoto Progetto IoT <br/></h2>
	        <h3>Misurazioni per paziente</h3>";  
	  $oggi=getdate();  
	   echo "Teramo ".$oggi["mday"]."-".$oggi["mon"] ."-".$oggi["year"];  
	?>
	<br/><br/>			
	<label>Paziente</label><br/>
	<select name="paziente" id="paziente">	
	<option>Seleziona</option>
	<?php
		// Query SQL per ottenere l'elenco dei pazienti del medico $_SESSION["id"] e 
        // popolare una  select da cui selezionare il paziente 
		$s="Select id,nomecognome	
		    from pazienti 
			where idmedico=$idmedico
		    order by nomecognome";
		$q=mysqli_query($conn,$s);
		$nr=mysqli_num_rows($q);
		$options="";
		if($nr>0){
			while($r = mysqli_fetch_array($q)){
				$options.="<option value=$r[0]>$r[1]</option>";
			}
			echo $options;
		} 
		?>
	</select>
    <br/><br/>Dal:<input type="date" name="data1">
	&nbsp;&nbsp;&nbsp;&nbsp;Al: <input type="date" name="data2">
	<br/><br/>
	<input type='submit' id="login" value='Submit'"/> 
	<input type='reset' id="reset" value='Reset'/> 
	<?php mysqli_close($conn)?>
  </body>  
</html>
<?php }
 else
	{
		$idpaziente=$_POST['paziente'];
		echo $idpaziente;
		$d1=$_POST["data1"];
		$d2=$_POST["data2"];
		$d2=date("Y-m-d",strtotime($d2."+1 days"));
		// occorre aggiungere un giorno alla data2
		$conn=mysqli_connect("localhost","root","","iotmedici");
		// Query SQL per ottenere i dati del paziente
		$s="Select  pazienti.id,pazienti.nomecognome,
		    pazienti.sesso,pazienti.dnascita,asl.nome 
		    from pazienti,asl 
			where pazienti.id=$idpaziente
			and pazienti.idasl=asl.id";
		$q=mysqli_query($conn,$s);
		$r = mysqli_fetch_array($q);
		$datanascita=date("d-m-Y",strtotime($r[3]));
		echo"<h2>Paziente: $r[1]</h2>Sesso: $r[2]<br/>
		     Data di nascita: $datanascita<br/>ASL: $r[4] <br/>";
	    echo "Intervallo temporale: ". date('d-m-Y', strtotime($d1)).
		       "   /   ".date('d-m-Y', strtotime($d2))."<br/>";
		// Query SQL per ottenere le misurazioni del paziente nell'intervallo
		// di tempo desiderato
		$s="SELECT  misurazioni.data_ora,
		   misurazioni.parametro,misurazioni.um,
		   misurazioni.valorerilevato,dispositivi.codice
		   from misurazioni, dispositivi
		   where misurazioni.idpaziente=$idpaziente
		   and misurazioni.codicedispositivo=dispositivi.codice
		   and misurazioni.data_ora  between '$d1'and '$d2'
		   order by misurazioni.data_ora";
		$q=mysqli_query($conn,$s);
		$nr=mysqli_num_rows($q);
		if($nr==0){
			echo "<br/>Nessuna misurazione trovata <br/><br/>";
		}
		else
		{
			$k=0;
			echo"<table>
				<tr bgcolor='#FFFF0F'><td>Nr</td><td>Data</td>
				<td>Ora</td>
				<td>Parametro</td><td>UM</td><td>Valore</td>
				<td>Codice dispositivo</td></tr>";
			while($r = mysqli_fetch_array($q))  
			{   
				$k++;
				$do=$r[0]; //data_ora
				$d=date('d-m-Y',strtotime($do));  //data
				$o=date('H:i:s', strtotime($do));  //ora
				echo"<tr>";
				echo"<td>$k</td>";echo"<td>$d</td>";
				echo"<td>$o</td>";echo"<td>$r[1]</td>";
				echo"<td>$r[2]</td>";echo"<td>$r[3]</td>";
				echo"<td>$r[4]</td>";
				echo"</tr>";
			}
			echo"</table>";
			echo"<br/>";		
		}
		mysqli_close($conn);
		echo"<a href='misurazioni.php'>Torna alla pagina precedente</a>";
	}	
?>






		

