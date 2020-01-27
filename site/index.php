<?php require "db.php"; ?>
<?php require "perevoditel 2000.php"; ?>
<?php if( isset($_SESSION['logged_user'])) : ?>
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
          <a href="index.php" class="navbar-brad"><img id="im" src="img/icon.png"></a>
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
                  <a href="logout.php">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Выйти</button>
                  </a>
                </li>
                <li class="nav-item mb-2">
                  <a href="panel.php">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit"><i class="fas fa-user"></i></button>
                  </a>
                </li>
              </ul>
          </div>
        </div>
      </nav>
    </header>
    <main class="mb-5 ml-2 mr-2">
      <div class="container mt-5 p-2 bg-dark rounded ">
        <div class="embed-responsive embed-responsive-16by9">
          <iframe src="<?php echo $aaa; ?>" class="embed-responsive-item rounded shadow" id="playground-property" style="filter: brightness(100%);" allowfullscreen></iframe>
        </div>
        <div class="row">
          <div class="col">
            <div class="mt-2">
              <input class="align-middle custom-range w-50" type="range" min="0" max="300" value="100" id="playground-value-input">
              <span class="text-white ml-3" id="playground-code-value">100%</span>
            </div>
          </div>
        </div>
        <!--https://www.youtube.com/embed/L_LUpnjgPso-->
        <!--<div class="mt-2">
          <input id="srcvid" name="nickname" placeholder="Введите ссылку" class="form-control">
          <button onclick="multi()"  class="btn btn-primary mt-2 mb-2" >Показать</button>
        </div>-->
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
    <script src="javascript.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" type="text/javascript"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <script src="https://use.fontawesome.com/releases/v5.0.8/js/all.js" type="text/javascript"></script>
  </body>
  <html>
<?php else : ?>
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
          <a href="index.php" class="navbar-brad"><img id="im" src="img/icon.png"></a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive">
            <span class="navbar-toggler-icon text-white">&#9776;</span>
          </button>
            <div class="collapse navbar-collapse mt-2" id="navbarResponsive">
              <ul class="navbar-nav m-auto">
                <li class="nav-item mb-2">
                  <a href="#" class="nav-link text-white">Обратная связь</a>
                </li>
                <li class="nav-item mb-2">
                  <a href="login.php">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Войти</button>
                  </a>
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
    <main class="mb-5 ml-2 mr-2">
      <div class="bg-dark rounded-lg" style="margin: 50px auto; max-width: 600px; width: 95%;">
        <div class="p-3">
          <h3 style="color:Silver;" class="text-center">Lorem ipsum dolor sit amet.</h3>
          <div><img class="w-100 rounded" src="img/banner.jpg" style="filter: brightness(50%);"></div>
          <p class="mt-3 text-white">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sit incidunt alias aperiam quos hic sapiente earum perspiciatis totam inventore, unde itaque voluptates! Necessitatibus illo dignissimos expedita, eum dicta recusandae sunt qui error aliquid! Expedita excepturi quasi eos atque, vitae nesciunt ab modi veniam dolores commodi non ea illo amet architecto, est totam minima eum sed ex repudiandae alias facilis aliquam nam. Quam provident qui sit. Consequatur sequi asperiores ea pariatur natus, dicta labore aliquam magnam, dolorem enim, similique quia illo vitae esse impedit nulla accusantium commodi velit dolore qui? Aspernatur dolores soluta esse, quos placeat temporibus ut molestiae ad omnis. Labore nostrum aliquid possimus, sit rem quasi quod necessitatibus ea quas officia voluptas nulla. Vel molestias, dicta neque, porro, at assumenda consectetur velit odit cum maiores nam similique rerum. Quia quae dolor sunt accusamus voluptates, possimus harum nesciunt veritatis praesentium obcaecati repellat provident consequatur, sint quos ut animi assumenda. Cum in impedit obcaecati, ea minus odio explicabo ab ipsum. Est maxime aliquam, architecto asperiores, velit error earum odit enim deserunt officiis maiores vero amet, dolorum blanditiis. Fugit, nam labore recusandae! Fuga culpa nesciunt accusamus id quas blanditiis minus recusandae, commodi, laboriosam repellendus quis cupiditate voluptates debitis, maxime reiciendis. Voluptatum dolor, inventore dolorem provident magnam aut nemo necessitatibus animi eligendi eos quam consequatur nisi eius omnis mollitia sunt minus quae deserunt delectus accusantium cumque porro ullam repudiandae. Quisquam eligendi nemo voluptate, beatae quas praesentium modi. Sequi accusantium odit, rerum labore modi perspiciatis asperiores autem ea soluta sunt temporibus dolorum, qui animi?
          </p>
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
    <script src="javascript.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" type="text/javascript"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <script src="https://use.fontawesome.com/releases/v5.0.8/js/all.js" type="text/javascript"></script>
  </body>
  <html>
<?php endif; ?>
