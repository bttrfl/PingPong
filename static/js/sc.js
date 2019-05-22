// класс определяющий параметры игрового прямоугольника и метод для его отрисовки

function rect(color, x, y, width, height) {
    this.color = color; // цвет прямоугольника
    this.x = x; // координата х
    this.y = y; // координата у
    this.width = width; // ширина
    this.height = height; // высота
    // функция рисует прямоугольник согласно заданным параметрам
    this.draw = function() {
        context.fillStyle = this.color;
        context.fillRect(this.x, this.y, this.width, this.height);
    };
}
// функция проверяет пересекаются ли переданные ей прямоугольные объекты

function collision(objA, objB) {
    return objA.x + objA.width > objB.x && objA.x < objB.x + objB.width && objA.y + objA.height > objB.y && objA.y < objB.y + objB.height
}
// движение игрока

function playerMove(e) {
    if (start) {
        var direction;
        if (e.keyCode == 38 || e.keyCode == 87) {
            socket.send(JSON.stringify({"event": "moveUp"}))
            direction = -1;
        }

        if (e.keyCode == 40 || e.keyCode == 83) {
            socket.send(JSON.stringify({"event": "moveDown"}))
            direction = 1;
        }
        update_y(player1, player1.y + direction*delta);
        // условие проверяет не выходит ли ракетка за пределы поля
    }
}

function update_y(player, y){
        if (0 < y && y < game.height - player.height) {
            player.y = y
        }
}

function startGame(pos) {
    if (pos == 2){
        tmp = player1
        player1 = player2
        player2 = tmp
    }
    if (!start) {
        ball.vX = -4;
        ball.vY = 4;
        start = true;
    }
}

// отрисовка игры

function draw() {
    game.draw(); // игровое поле
    // разделительная полоса
    for (var i = 10; i < game.height; i += 45) {
        context.fillStyle = "#ccc";
        context.fillRect(game.width / 2 - 10, i, 20, 30);
    }
    // рисуем на поле счёт
    context.font = 'bold 128px courier';
    context.textAlign = 'center';
    context.textBaseline = 'top';
    context.fillStyle = '#ccc';
    context.fillText(player2.scores, 100, 0);
    context.fillText(player1.scores, game.width - 100, 0);
    player2.draw(); // левая ракетка
    player1.draw(); // ракетка игрока
    ball.draw(); // шарик
    if (!start) {
    }
}
// игровые изменения которые нужно произвести

function update() {
    // двигаем ракетку оппонента
    // меняем координаты шарика
    // Движение по оси У
    if (ball.y < 0 || ball.y + ball.height > game.height) {
        // соприкосновение с полом и потолком игрового поля
        ball.vY = -ball.vY;
    }
    // Движение по оси Х
    if (ball.x < 0) {
        // столкновение с левой стеной
        ball.vX = -ball.vX;
        player1.scores++;
    }
    if (ball.x + ball.width > game.width) {
        // столкновение с правой
        ball.vX = -ball.vX;
        player2.scores++;
    }

    // Если счёт равен десяти то завершаем партию
    if (player2.scores === 10 || player1.scores === 10) {
        if (player2.scores === 10) { // победа player2
            start = false;
            ball.x = game.width - player1.width - 1.5 * ball.width - 10;
            ball.y = game.height / 2 - ball.width / 2;
            player2.y = game.height / 2 - player2.height / 2;
            player1.y = game.height / 2 - player2.height / 2;
        } else { // победа игрока
            start = false;
            ball.x = player1.width + ball.width;
            ball.y = game.height / 2 - ball.width / 2;
            player2.y = game.height / 2 - player2.height / 2;
            player1.y = game.height / 2 - player2.height / 2;
        }
        ball.vX = 0;
        ball.vY = 0;
        player2.scores = 0;
        player1.scores = 0;
    }

    // Соприкосновение с ракетками
    if ((collision(player2, ball) && ball.vX < 0) || (collision(player1, ball) && ball.vX > 0)) {
        ball.vX = -ball.vX;
    }
    ball.x += ball.vX;
    ball.y += ball.vY;

    console.log(player1, player2, ball)
}

function play() {
    draw(); // отрисовываем всё на холсте
    update(); // обновляем координаты
}
// Инициализация переменных

function init() {
    start = false;
    // объект который задаёт игровое поле
    game = new rect("#000", 0, 0, 800, 600);
    // Ракетки-игроки
    player2 = new rect("#ffffff", 10, game.height / 2 - 40, 20, 80);
    player1 = new rect("#ffffff", game.width - 30, game.height / 2 - 40, 20, 80);
    // количество очков
    player2.scores = 0;
    player1.scores = 0;
    // наш квадратный игровой "шарик"
    ball = new rect("#fff", 40, game.height / 2 - 10, 20, 20);
    // скорость шарика
    ball.vX = 0; // скорость по оси х
    ball.vY = 0; // скорость по оси у
    delta = 40;
    ball.x = game.width/2;
    ball.y = game.height/2;
    var canvas = document.getElementById("canvas");
    canvas.width = game.width;
    canvas.height = game.height;
    context = canvas.getContext("2d");
    window.addEventListener("keydown", playerMove, false);
    setInterval(play, 1000 / 50);
}
