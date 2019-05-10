
var popWin = {
    scrolling: 'no',
    //是否显示滚动条 no,yes,auto

int: function() {
        this.mouseClose();
        this.closeMask();
        //this.mouseDown();

    },

showWin: function(width, height, title, src) {
        var iframeHeight = height - 52;
        var marginLeft = width / 2;
        var marginTop = height / 2;
        var inntHtml = '';
        inntHtml += '<div id="mask" style="width:100%; height:100%; position:fixed; top:0; left:0; z-inde:1999;background:#cccccc; filter:alpha(opacity=50); -moz-opacity:0.5; -khtml-opacity: 0.5; opacity:0.5;"></div>'
        inntHtml += '<div id="maskTop" style="width: ' + width + 'px; height: ' + height + 'px; border: #999999 1px solid; background: #fff; color: #333; position: fixed; top: 50%; left: 50%; margin-left: -' + marginLeft + 'px; margin-top: -' + marginTop + 'px; z-index: 2999; filter: progid:DXImageTransform.Microsoft.Shadow(color=#909090,direction=120,strength=4); -moz-box-shadow: 2px 2px 10px #909090; -webkit-box-shadow: 2px 2px 10px #909090; box-shadow: 2px 2px 10px #909090;">'
        inntHtml += '<div id="maskTitle" style="height: 150px; line-height: 150px; font-family: Microsoft Yahei; font-size: 20px; color: #333333; padding-left: 20px; background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAyCAYAAABlG0p9AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABvSURBVEhL1cq5DcAwDENR7T+sL9lOOoUbkCoCwwKewOJbiGe+31BkwgeDM18YgrPhxuBs4CkS4cQQZMKFwd0R+gzFJaFjcD+EfXgoMuHA4O4Iew/FJWHD4BJhwxDoYcNTIKwY3NGwYggQFgxODEt8xO1/6P+HHxEAAAAASUVORK5CYII=); border-bottom: 1px solid #999999; position: relative;">'
        inntHtml += '' + title + ''
        inntHtml += '<div id="popWinClose" style="width: 28px; height: 28px; cursor: pointer; position: absolute; top: -12px; right: -9px; background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJeSURBVEhLvZbPq2lRFMf9B4bSTTIxZiBSMlCI9ycoKX+Bod7w/il3YIL4NyhFmYmBKD2Sp0ix3vqes/e529n74t33Op9astevr3PO2tvxvcLtdquzfbAtyAV8IlYX6d+DG7yxvbP9Fr2fglxR8ybavAYX/GD7Jfr8NahFD9HuMZz4U9Q5jEYjqlarFA6HiVPuDD7EkOMGvTjna9xi8/mcstmsJvKVIRc1Kl+K4haIHItut0t+v9/Y+JGhBrUq6M2xT9iBAXGeGQrY/U+miqI3NNhvw4t3EbNuyXeuzG3ood5eaLDfhhfO6JueWbPZtGKFQkGLNRoN2u/3FI/HtRh6SaDBPkusLnzWpMlkaRC7XC5WfLVaUTqddmKVSoVOp5MVG4/HlEql7mph6vRCC4IfYm2Nt7vAzW63o2KxSLVaja7Xq/DatFotrR49JdCCoHNcmfZZPp+n9XotMmxwVVwnVjbD4ZAikYhWj54SaN1dgjtZWiaToe12K7J0JpOJUUyaykuCsFwuR8fjUWR+slgsKBAIGGukqbwsiGdmElwul5RIJIw10lReEsQ0ns9nkaVzOBys226qhak8HRrsM7ktJLPZjDabjVjZYLBKpZJWrw0NfzzcFvj1KtPp1HpmsVjM2iIq/X5fqzdti4cbHycINjUYDAYUCoWcGA4BHAag1+tRMBi8q4VpGx/wl4dHWzKZpHa7TdFoVIuVy2XqdDrGSTUebYAXnh/e3v49AXZ49wcs4YB3rxgStyjApGG8TfsUPsTUaZQ8FZPgFrB585oo4QLvXoTdcIP/9Krv8/0BDUSOirKWU6wAAAAASUVORK5CYII=);"></div>'
        inntHtml += '</div>'
        inntHtml += '<iframe width="' + width + '" height="' + iframeHeight + '" frameborder="0" scrolling="' + this.scrolling + '" src="' + src + '"></iframe>';

        $("body").append(inntHtml);
        this.int();


    },

mouseClose: function() {
        $("#popWinClose").on('mouseenter', 
        function() {
            $(this).css("background-image", "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJwSURBVEhLvZbLSiNBFIb7DVyKiIgb17oQRRAXgor6CIIIeQKXMksfxYUbFbMZRh0Yb6ODMgEddCVmoWkRLzFekukxfay/+lRbqSqTVob+4CyqzuVPV59TaS8JYRhmhM0Ly5MB9tiX4fDPIQq0CpsT9sC1G4JYzmnlMskQCRPCrrnOh0EuanC5+ojAL5wXc5/LUW5qitba2ynreTWGPfgQY4JaXNaNKfZ0dkY7g4OWyHuGWOTovCuKI+AYib+8TF+bmpyF6xlykKuD2iwTITbQIPE7Q4Kr2EdMF0VtaLCcFJxjnzySzzyZaaihHy80WE4Kxq3vemcns7PStzsyYvn+zMxQUCzSRne35UMtBTSUWIb3ZKeZSRCrBoH0lwsF2u7vj32/JyepWi5L3/3hIW319dXkwvTuhRYE53kt29tMMAlub2lvdJRy09MUVqu8G3GxsGDlo6YCWhCMryvXnO0OD1PF9zkiQj5VGPIqonhwQOsdHVY+aiqgVfMIZrCy7YEBCm5uOMqmdHTkFFOmk0gQ9nNoiF4eHznyjed8nr41NztzlOkkFsQ7cwmWz89ps6fHmaNMJ5Gg7MZKhaNs/pVK8thduTCdhk2DOVNjoXg6PaW/V1e8ikBj7Y2NWflW06BVee0cC/x6nYfjY/nOfnR1yRHRucxmrXzXWNQdfNwgGGpwt79Pa21tsQ+XAC4D4K+s0GpLS00uzBp8vm3qXm1bvb1UWFyk752dlu/X+Dj5S0vOTnVebUAsUr+80/17AmIjvT9ghXCk94mhMEUBOg3t7ZpT7MGnd6OioZgCRyAsnc9EhUhI70PYRBT4T5/6nvcKYG1hElXAZggAAAAASUVORK5CYII=)");

        });

        $("#popWinClose").on('mouseleave', 
        function() {
            $(this).css("background-image", "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJeSURBVEhLvZbPq2lRFMf9B4bSTTIxZiBSMlCI9ycoKX+Bod7w/il3YIL4NyhFmYmBKD2Sp0ix3vqes/e529n74t33Op9astevr3PO2tvxvcLtdquzfbAtyAV8IlYX6d+DG7yxvbP9Fr2fglxR8ybavAYX/GD7Jfr8NahFD9HuMZz4U9Q5jEYjqlarFA6HiVPuDD7EkOMGvTjna9xi8/mcstmsJvKVIRc1Kl+K4haIHItut0t+v9/Y+JGhBrUq6M2xT9iBAXGeGQrY/U+miqI3NNhvw4t3EbNuyXeuzG3ood5eaLDfhhfO6JueWbPZtGKFQkGLNRoN2u/3FI/HtRh6SaDBPkusLnzWpMlkaRC7XC5WfLVaUTqddmKVSoVOp5MVG4/HlEql7mph6vRCC4IfYm2Nt7vAzW63o2KxSLVaja7Xq/DatFotrR49JdCCoHNcmfZZPp+n9XotMmxwVVwnVjbD4ZAikYhWj54SaN1dgjtZWiaToe12K7J0JpOJUUyaykuCsFwuR8fjUWR+slgsKBAIGGukqbwsiGdmElwul5RIJIw10lReEsQ0ns9nkaVzOBys226qhak8HRrsM7ktJLPZjDabjVjZYLBKpZJWrw0NfzzcFvj1KtPp1HpmsVjM2iIq/X5fqzdti4cbHycINjUYDAYUCoWcGA4BHAag1+tRMBi8q4VpGx/wl4dHWzKZpHa7TdFoVIuVy2XqdDrGSTUebYAXnh/e3v49AXZ49wcs4YB3rxgStyjApGG8TfsUPsTUaZQ8FZPgFrB585oo4QLvXoTdcIP/9Krv8/0BDUSOirKWU6wAAAAASUVORK5CYII=)");

        });

    },

closeMask: function() {
        $("#popWinClose").on('click', 
        function() {
            $("#mask,#maskTop").fadeOut(function() {
                $(this).remove();

            });

        });

    }

/*mouseDown : function(){
		var dragging = false;
		var iX, iY;
		//var elmen = $("div#maskTop");
		$("#maskTop").on('mousedown' , function(e){
			dragging = true;
                iX = e.clientX - this.offsetLeft;
                iY = e.clientY - this.offsetTop;
                this.setCapture && this.setCapture();
                return false;
		});
		document.onmousemove = function(e) {
                if (dragging) {
                var e = e || window.event;
                var oX = e.clientX - iX;
                var oY = e.clientY - iY;
                $("#maskTop").css({"left":oX + "px", "top":oY + "px"});
                return false;
                }
            };
            $(document).mouseup(function(e) {
                dragging = false;
                $("#maskTop")[0].releaseCapture();
                e.cancelBubble = true;
            })
	},*/

};