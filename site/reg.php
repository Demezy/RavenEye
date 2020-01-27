<?php
  require "db.php";

  $data = $_POST;
  if( isset($data['do_reg']) )
  {
    $errors = array();
    if ( trim($data['nickname']) == '' )
    {
      $errors[] = 'Введите nickname';
    }

    if ( $data['pass'] == '' )
    {
      $errors[] = 'Введите пароль';
    }

    if ( $data['pass2'] != $data['pass'] )
    {
      $errors[] = 'Повторный пароль введён не верно!';
    }

    if ( R::count('users', "login = ?", array($data['nickname'])) > 0 )
    {
      $errors[] = 'Пользователь с таким ником уже существует';
    }

	function KeyGen(){
      $key = md5(mktime());
      $new_key = '';
      for($i=1; $i <= 25; $i ++ ){
        $new_key .= $key[$i];
        if ( $i%5==0 && $i != 25) $new_key.='-';
      }
      return strtoupper($new_key);
    }

    if ( empty($errors) )
    {
      $user = R::dispense('users');
      $user->login = $data['nickname'];
      $user->email = $data['email'];
      $user->password = password_hash($data['pass'], PASSWORD_DEFAULT);
      $user->code = KeyGen();
      R::store($user);
      $zar = 'Вы успешно зарегистрированы!';
      $data['nickname'] = '';
      $data['email'] = '';
      $data['pass'] = '';
      $data['pass2'] = '';
    } else
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
<body class="h-100" style="background-color:gray;">
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
                <a href="login.php">
                  <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Войти</button>
                </a>
              </li>
            </ul>
        </div>
      </div>
    </nav>
  </header>
  <main class="">
    <div class="bg-dark rounded-lg" style="margin: 50px auto; max-width: 500px; width: 95%;">
      <div class="p-5" style="width: 95%; margin: 50px auto;">
        <form action="reg.php" method="POST">
          <div class="mb-2 rounded-lg" style="color: red; background-color:Silver;"><?php echo($err) ?></div>
          <p><input name="nickname" placeholder="Nickname" class="form-control" value="<?php echo @$data['nickname']; ?>"></p>
          <p><input type="email" name="email" placeholder="Email" class="form-control mt-2" value="<?php echo @$data['email']; ?>"></p>
          <p><input name="pass" type="password" id="pass" placeholder="Password" class="form-control mt-2" value="<?php echo @$data['pass']; ?>"></p>
          <p><input name="pass2" type="password" placeholder="Password again" class="form-control mt-2" value="<?php echo @$data['pass2']; ?>"></p>
          <p><button type="submit" id="login" name="do_reg" class="btn mt-2 btn-success">Зарегистрироваться</button></p>
          <div class="rounded-lg" style="color: green; background-color:Silver;"><?php echo($zar) ?></div>
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
