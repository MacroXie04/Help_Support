document.addEventListener('DOMContentLoaded', function () {
    // 使用 querySelectorAll 选取所有具有 'timer' 类和 'timer' ID 的元素
    var timerElements = document.querySelectorAll('.timer[id="timer"]');

    // 遍历每个计时器元素
    timerElements.forEach(function (timberElement) {
        // 获取日期字符串，优先从 data-time 属性中获取
        var dateString = timberElement.getAttribute('data-time');
        if (!dateString) {
            console.error('No data-time attribute found for element', timberElement);
            timberElement.innerText = "No Due Date";
            return;
        }

        // 将日期字符串解析为 Date 对象
        var countDownDate = new Date(dateString);
        if (isNaN(countDownDate.getTime())) {
            timberElement.innerText = "Invalid Due Date";
            return;
        }

        // 开始倒计时
        var x = setInterval(function () {
            var now = new Date().getTime();
            var distance = countDownDate - now;

            if (distance < 0) {
                clearInterval(x);
                timberElement.innerText = "Due Date has passed";
                return;
            }

            // 计算剩余的天、小时、分钟、秒
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // 根据剩余时间调整显示
            if (distance < 60 * 60 * 1000) {
                // 小于1小时
                timberElement.innerText = minutes + " minutes " + seconds + " seconds";
            } else if (distance < 24 * 60 * 60 * 1000) {
                // 小于24小时
                timberElement.innerText = hours + " hours " + minutes + " minutes";
            } else {
                // 大于1天
                timberElement.innerText = days + " days " + hours + " hours";
            }

        }, 1000);
    });
});