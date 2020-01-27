<?php
  require "db.php";

  $data = $_POST;
  if( isset($data['do_login']) )
  {
    $errors = array();
    $user = R::findOne('users', 'login = ?', array($data['nickname']) );
    if ( $user )
    {
      if ( password_verify($data['pass'], $user->password))
      {
        $_SESSION['logged_user'] = $user;
        $zar = 'Вы успешно вошли';
        header('Location: index.php');
      } else
      {
        $errors[] = 'Неверный пароль';
      }
    } else {
      $errors[] = 'Пользователь с таким ником не найден';
    }

    if ( !empty($errors) )
    {
      $err = array_shift($errors);
    }

  }
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
              <li class="nav-item mb-2">
                <a href="reg.php">
                  <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Регистрация</button>
                </a>
              </li>
            </ul>
        </div>
      </div>
    </nav>
  </header>
  <main>
    <div class="bg-dark rounded-lg" style="width: 95%; margin: 50px auto; max-width: 500px;">
      <div class="p-2" style="width: 95%; margin: 50px auto;">
        <h4 class="text-center mb-4 text-white"> Форма входа </h4>
        <form action="login.php" method="POST" class="">
          <div class="mb-2 rounded-lg" style="color: red; background-color:Silver;"><?php echo($err) ?></div>
          <input name="nickname" placeholder="Nickname" class="form-control">
          <input name="pass" type="password" id="pass" placeholder="Password" class="form-control mt-2">
          <button type="submit" id="login" name="do_login" class="btn btn-success mt-2">Войти</button>
          <div class="rounded-lg mt-2" style="color: green; background-color:Silver;"><?php echo($zar) ?></div>
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
