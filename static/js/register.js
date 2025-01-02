$(function() {
    function ButtonClick() {
        $('#validation-btn').click(function(event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("Please enter valid email");
                return;
            }
            $this.off('click');
            $.ajax('/auth/validate?email=' + email, {
                method: 'GET',
                success: function(result) {
                    if (result['code'] == 200) {
                        alert("Email sent successfully!");
                    }
                    else {
                        alert(result['message']);
                    }
                },
                fail: function(error) {
                    console.log(error);
                }
            })
            let countdown = 6;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text("obtain");
                    clearInterval(timer);
                    ButtonClick();
                } else {
                    countdown--;
                    $this.text(countdown + "s");
                }
            }, 1000);
        })
    }
    ButtonClick();
});