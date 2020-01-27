<?php
  require "db.php";
  $data = $_POST;
  $id = $_SESSION['logged_user']->id;
  $mysqli = new mysqli('127.0.0.1', 'mysql', 'mysql', 'my2');
  if( isset($data['do_update']) )
  {
    $errors = array();
    if ( trim($data['nickname']) == '' )
    {
      $errors[] = 'Введите nickname';
    }

    if (( R::count('users', "login = ?", array($data['nickname'])) > 0) and ((R::getAll("SELECT login FROM users WHERE id = '$id'")[0]['login']) != $data['nickname']) )
    {
      $errors[] = 'Пользователь с таким ником уже существует';
    } else
	{
	  $mysqli->query("UPDATE `users` SET `login` = '{$data['nickname']}' WHERE id = '$id'");
	}

	if (( R::count('users', "login = ?", array($data['nickname'])) > 0) and ((R::getAll("SELECT login FROM users WHERE id = '$id'")[0]['login']) != $data['nickname']) )
    {
      $errors[] = 'Пользователь с таким ником уже существует';
    } else
	{
	  $mysqli->query("UPDATE `users` SET `login` = '{$data['nickname']}' WHERE id = '$id'");
	}

	if (($data['pass'] == '') and ($data['newpass'] == '') and ($data['newpass2'] == ''))
	{

    } elseif ( (password_verify($data['pass'], R::getAll("SELECT password FROM users WHERE id = '$id'")[0]['password'])))
	{
	  if ( ($data['newpass2'] != $data['newpass']) and ($data['newpass'] != '') and ($data['newpass2'] != '') )
      {
        $errors[] = 'Повторный пароль введён не верно!';
      } elseif ($data['newpass'] == '')
	  {
	    $errors[] = 'Введите новый пароль';
	  } elseif ($data['newpass2'] == '')
	  {
	    $errors[] = 'Повторите новый пароль';
	  } else
	  {
	    $password = password_hash($data['newpass'], PASSWORD_DEFAULT);
	    $mysqli->query("UPDATE `users` SET `password` = '$password' WHERE id = '$id'");
	  }
	} elseif (($data['newpass2'] == $data['newpass']) and ($data['pass'] == ''))
	{
      $errors[] = 'Введите старый пароль';
	} elseif (($data['newpass2'] != $data['newpass']) and ($data['pass'] == ''))
	{
      $errors[] = 'Введите старый пароль';
	} else
	{
	  $errors[] = 'Старый пароль введён неверно';
	}

	if (($data['email'] != '') and ((R::getAll("SELECT email FROM users WHERE id = '$id'")[0]['email']) != $data['email']))
	{
	  $mysqli->query("UPDATE `users` SET `email` = '{$data['email']}' WHERE id = '$id'");
	}

    if ( empty($errors) )
    {
	  //$query = "SELECT `login` FROM `users`";
      //$user->email = $data['email'];
      //$user->password = password_hash($data['pass'], PASSWORD_DEFAULT);
      //$user->code = '';
	  $up = 'Данные успешно обновлены!';
	  //$nick = mysqli_query($mysqli, $query);
    } else
    {
      $err = array_shift($errors);
    }
  }

?>
<?php if( isset($_SESSION['logged_user'])) : ?>
<?php
  $id = $_SESSION['logged_user']->id;
  $user_nick = R::getAll("SELECT login FROM users WHERE id = '$id'");
  $user_email = R::getAll("SELECT email FROM users WHERE id = '$id'");
  $user_code = R::getAll("SELECT code FROM users WHERE id = '$id'");
  $login = $user_nick [0]['login'];
  $email = $user_email [0]['email'];
  $code = $user_code [0]['code'];
?>
  <!DOCTYPE html>
  <html lang="ru">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="keywords" content="">
    <meta name="description" content="">
    <title>Informatics Project</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="img/icon.png" sizes="16x16" type="image/png">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
  </head>
  <body style="background-color:gray;">
    <header class="">
      <nav class="navbar navbar-expand-md bg-dark sticky-top">
        <div class="container-fluid">
          <a href="index.php" class="navbar-brad"><img src="img/icon.png"></a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive">
            <span class="navbar-toggler-icon text-white">&#9776;</span>
          </button>
            <div class="collapse navbar-collapse mt-2" id="navbarResponsive">
              <ul class="navbar-nav m-auto">
                <li class="nav-item active mb-2">
                  <a href="index.php" class="nav-link text-white">Трансляция</a>
                </li>
                <li class="nav-item mb-2">
                  <a href="#" class="nav-link text-white">Обратная связь</a>
                </li>
              </ul>
          </div>
        </div>
      </nav>
    </header>
    <main>
      <div class="bg-dark rounded-lg" style="width: 95%; margin: 50px auto; max-width: 500px;">
        <div class="p-2 text-white" style="width: 95%; margin: 50px auto;">
          <h4 class="text-center mb-4 text-white"> Здесь располагаются Ваши данные, которые Вы можете обновлять </h4>
          <form action="panel.php" method="POST" class="">
            <p>Nickname:<input name="nickname" placeholder="Nickname" class="form-control" value="<?php echo $login; ?>"></p>
            <p>Email:<input name="email" placeholder="Email" class="form-control" value="<?php echo $email; ?>"></p>
            <p>(чтобы обновить пароль введите старый пароль)<br>Пароль:<input name="pass" type="password" id="pass" placeholder="Password" class="form-control"></p>
            <p>Новый пароль:<input name="newpass" type="password" id="pass" placeholder="New Password" class="form-control"></p>
            <p>Новый пароль:<input name="newpass2" type="password" id="pass" placeholder="New Password" class="form-control"></p>
            <p>(пока что недействителен)<br>Код для входа в Telegram бота:<input name="pass" id="pass" class="form-control" value="<?php echo $code; ?>" disabled></p>
            <div class="rounded-lg mt-2" style="color: green; background-color:Silver;"><?php echo($up) ?></div>
			<div class="mb-2 rounded-lg" style="color: red; background-color:Silver;"><?php echo($err) ?></div>
            <button type="submit" id="login" name="do_update" class="btn btn-success mt-2">Сохранить</button>
          </form>
        </div>
      </div>
    </main>
    <footer class="container-fluid bg-dark p-3 text-white">
      <div class="container">
        <div class="row padding text-center">
          <div class="col-12">
            <p>&copy; Project by Lehin and Nikita</p>
            <p>Чтобы узнать больше, обратитесь куда-нибудь<a href="mailto:comailru@mail.ru"><img class="ml-2" style="width: 25px; height: 25px;" src="img/mail1.png" alt=""></a></p>
          </div>
        </div>
      </div>
    </footer>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" type="text/javascript"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <script src="https://use.fontawesome.com/releases/v5.0.8/js/all.js" type="text/javascript"></script>
  </body>
  <html>
 <?php else : header('Location: index.php');?>
 <?php endif; ?>
