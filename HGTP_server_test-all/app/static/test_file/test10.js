        var $SCRIPT_ROOT = 'http://'+window.location.host
        //创建接口文档操作
        var t = Date.now();

function sleep(d){
    while(Date.now - t <= d);
}
        //提交要遍历的url
        $('button[name][id]').click(function () {
                if ($(this).attr('class') == 'btn btn-default') {
                    $(this).attr('class', 'btn btn-default btn-success')
                }
                else {
                    $(this).attr('class', 'btn btn-default')
                }
            }
        )
        //下拉列表选择
        $('.dropdown-menu>li').click(function () {
                $(this).parent().parent().find('a').eq(0).html($(this).find('a').html())
            }
        )
        //checkbox全选
        $('#allcheck').click(function () {
                if ($('#allcheck').is(':checked')) {
                    $('input[name="childcheck"]').each(function () {
                            if (!$(this).is(':hidden')) {
                                $(this).attr('checked', true)
                            }
                        }
                    )
                }
                else {
                    $('input[name="childcheck"]').attr('checked', false)
                }
            }
        )
        //选个单个
        $('#format').find('button').click(function () {
            var a = 1
            $('#table4').find('tr:gt(0)').each(function () {
                    var name = $(this).find('td').eq(1).text()
                    if ($('button[name="' + name + '"' + "]").attr('class') == 'btn btn-default btn-success') {
                        a = 2
                        $(this).show()
                    }
                    else {
                        $(this).hide()
                    }
                }
            )
            if (a == 1) {
                $('#table4').find('tr').show()
            }
        })
        //监听第一个搜索框内容发生改变
        $("#check_1").bind("DOMNodeInserted", function (e) {
            var name = $(this).html()
            $("#check_2").find('a').html('all')
            $('#table4').find('tr:gt(0)').hide()
            $('#table4').find('tr[name="' + name + '"]').show()
//后面的搜索框根据前面的选择显示
            $('#selecttwo').find('li').hide()
                $('#selecttwo').find('li').each(function () {

                        if ($(this).attr('name') == name || $(this).attr('name')=='all') {
                            $(this).show()
                        }
                    }
                )

            if (name=='all')
            {
                $('#table4').find('tr:gt(0)').show()
            }
        })
        //监听第二个搜索框内容发生改变
        $("#selecttwo").bind("DOMNodeInserted", function (e) {
            name = $(this).find('a').html()
            $('#table4').find('tr:gt(0)').hide()
            if (name!='all') {
                $('#table4').find('tr[class="' + name + '"]').show()
            }
            else
            {
                name=$("#check_1").html()
                $('#table4').find('tr[name="' + name + '"]').show()
            }
        })
        //获取所有checke的接口信息
        $('#pilaing_yunxing').click(function () {
                var all_mulu = []
                $('input[name="childcheck"]').each(function () {
                        if ($(this).is(':checked')) {
                            all_mulu.push($(this).attr('class'))
                        }
                    }
                )
                if (all_mulu.length==0)
                {

                   layer.msg('没有选择运行接口', {icon: '2'})
                }
                else
                {
                    $('#run_result_open').html('运行中')
            $('#run_result_open').attr('disabled',true)
                $("this").attr("disabled", true);
                layer.msg('开始运行', {icon: '1'})
                var all_mulu = JSON.stringify({'all_mulu': all_mulu})
                var huanjing = $('#check_0').html()
                var gen_mulu = $.cookie('genmulu')
                var ip_dizhi = $('#tag_shuruip').attr('name')
                $.post($SCRIPT_ROOT + '/piliang_run', {
                        all_jiekou_re: all_mulu,
                        huanjing: huanjing,
                        gen_mulu: gen_mulu,
                        ip_dizhi: ip_dizhi
                    },
                    function (data) {

                    }
                )
            check_statu = setInterval("run_statu()",1000);
                }
            }
        )
        //单个接口跑
        $('button[name="simple_run_list"]').click(function () {
                $('#run_result_open').html('运行中')
            $('#run_result_open').attr('disabled',true)
                var all_mulu = []
                all_mulu.push($(this).parent().parent().find('td>input').attr('class'))
                var all_mulu = JSON.stringify({'all_mulu': all_mulu})
                var huanjing = $('#check_0').html()
                var gen_mulu = $.cookie('genmulu')
                var ip_dizhi = $('#tag_shuruip').attr('name')
                layer.msg('开始运行', {icon: '1'})
                $.post($SCRIPT_ROOT + '/piliang_run', {
                        all_jiekou_re: all_mulu,
                        huanjing: huanjing,
                        gen_mulu: gen_mulu,
                        ip_dizhi: ip_dizhi
                    },
                    function (data) {
                    }
                )
                            //发送是否运行中请求获取函数

              check_statu = setInterval("run_statu()",1000);

            }
        )


                      function  run_statu() {
                      if ($('#run_result_open').text()!='查看运行结果')
                      {
                   $.get($SCRIPT_ROOT + '/piliang_run_over', {
                        type:'is_running'
                    },
                    function (data) {
                       if (data.run_statu==2)
                       {

                           $('#run_result_open').html('查看运行结果')
                           $('#run_result_open').attr('disabled',false)

                       }
                    }

                )
                }

              }

        //环境checkbox发生变化时，发出请求，更新页面
        $("#check_0").bind("DOMNodeInserted", function (e) {
            huanjing = $(this).html()
            all_mulu = $.cookie('genmulu')
            ip_dizhi = $('#tag_shuruip').attr('name')
            $.post($SCRIPT_ROOT + '/uplate_jiekou_list', {mulu: all_mulu, huanjing: huanjing, ip_dizhi: ip_dizhi},
                function (data) {
                    window.location.reload()
                }
            )
        })


        //bootstrap弹出框
        $(function () {
            $("[data-toggle='popover']").popover({delay: {"show": 5000, "hide": 100}});
        });


        //点击打开结果页面

        $('#run_result_open').click(function () {


               window.open($SCRIPT_ROOT + '/jie_kou')

            }
        )


        //点击页面表格后面的调试按钮进入调试页面
        $('button[name="tiaoshi_tiaozhuan"]').each(function () {
            $(this).click(function () {
                    mulu = $(this).find('span').attr('name')
                    var huanjing = $('#check_0').html()
                    var gen_mulu = $.cookie('genmulu')

                    $.post($SCRIPT_ROOT + '/jiekou_mulu', {mulu: mulu, statu: "调试", huanjing: huanjing, gen_mulu: gen_mulu},
                        function (data) {


                            window.location.replace($SCRIPT_ROOT + '/shishitiaoshi')
                        }
                    )
                }
            )
        })
    //点击关联ip按钮
     $('#submit_guanlian_ip').click(function()
         {
                                $.post($SCRIPT_ROOT + '/guanlian_ip', {type:"guanlian_ip",ip_dizhi:$('#ip_guanlian').val()},
                        function (data) {
                           layer.msg('关联成功', {icon: '1'})

                        }
                    )

         }
     )

    //公共config读取
         $('a[href="#ios"]').on('shown.bs.tab', function (e) {
             var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="file_secret_publick"]').find('select').val()
             var yewu=$('div[name="file_yewu_publick"]').find('select').val()
             var json_data = $('#json_template_publick').html()
             var gen_mulu=$.cookie('genmulu')
                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"publick_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_publick').html(data.data)

                        }

             )


        })


                $('select[name="publick_config_change"]').bind("change",function () {
                    sleep(200)
                                 var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="file_secret_publick"]').find('select').val()
             var yewu=$('div[name="file_yewu_publick"]').find('select').val()
             var json_data = $('#json_template_publick').html()
             var gen_mulu=$.cookie('genmulu')
                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"publick_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_publick').html(data.data)

                        }

             )


                })

    //private_config读取
         $('a[href="#private_config"]').on('shown.bs.tab', function (e) {
             var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="private_config_file"]').find('select').val()
             var yewu=$('div[name="file_yewu_private"]').find('select').val()
             var jiekou=$('div[name="file_yewu_private"]').eq(1).find('select').val()
             var json_data = $('#json_template_private').html()
             var gen_mulu=$.cookie('genmulu')
                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"private_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data,jiekou:jiekou},
                        function (data) {
                           $('#json_moban_private').html(data.data_json)
                            $('#json_template_private').html(data.data_config)
                            $("#private_select_jjiekou_select").empty()
                            for (var i=0;i<data.jiekou_list.length;i++)
                            {

                                $("#private_select_jjiekou_select").append('<option>'+data.jiekou_list[i]+'</option>')

                            }

                        }

             )


        })


                $('select[name="private_config_change"]').bind("change",function () {
                    sleep(200)
                                 var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="file_secret_private"]').find('select').val()
             var yewu=$('div[name="file_yewu_private"]').find('select').val()
             var json_data = $('#json_template_private').html()
             var gen_mulu=$.cookie('genmulu')
                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"private_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_private').html(data.data)
                        }
             )
                })
    //显示数据库配置文件
    $('a[href="#jmeter"]').on('show.bs.tab', function (e) {
                     var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="file_secret_db"]').find('select').val()
             var yewu=$('div[name="file_yewu_db"]').find('select').val()
        var json_data = $('#json_template_db').html()
         var gen_mulu=$.cookie('genmulu')
                $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"db_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_db').html(data.data)
                        }
             )


})



                $('select[name="db_config_change"]').bind("change",function () {
                    sleep(200)
                         var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="file_secret_db"]').find('select').val()
             var yewu=$('div[name="file_yewu_db"]').find('select').val()
        var json_data = $('#json_template_db').html()
         var gen_mulu=$.cookie('genmulu')
                $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port')+ '/read_config', {type:"db_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_db').html(data.data)

                        }

             )


                })

    //打开excel
        $('button[name="open_file"]').each(function(){


            $(this).click(function(){
                         var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('#check_0').html()
                var jiekou_name=$(this).parent().attr('name')
                var yewu=$(this).parent().prev().prev().prev().prev().html()
         var gen_mulu=$.cookie('genmulu')

                                $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/open_excel', {type:"open_excel",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,jiekou_name:jiekou_name},
                        function (data) {
                               $('#json_template_db').html(data.data)

                        }

             )



            })})

        //弹出框创建配置文件，接口配置文件，更改业务名，更改接口列表显示
        $('select[name="file_yewu_private_select"]').eq(1).change(function(){
            var yewu=$(this).val()
            var  statu=0
            $('select[name="file_yewu_private_select"]').eq(2).find('option').each(function(){
                if ($(this).attr('name')!=yewu)
                {
                    $(this).hide()
                }
                else
                {
                    $(this).show()
                    if (statu==0)
                    {
                        $(this).attr('selected',true)
                        statu=1
                    }
                }
            })
        })



        //接口配置，如果修改接口名称，发送请求更改显示内容
        $('select[name="file_yewu_private_select"]').eq(2).change(function(){
           sleep(200)
            var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="private_config_file"]').find('select').val()
            var yewu=$('div[name="file_yewu_private"]').find('select').val()
            var jiekou=$('div[name="file_yewu_private"]').eq(1).find('select').val()
            var json_data = $('#json_template_private').html()
            var gen_mulu=$.cookie('genmulu')
            $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"private_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data,jiekou:jiekou},
                function (data) {
                    $('#json_template_private').html(data.data_config)
                    $('#json_moban_private').html(data.data_json)

                }

            )

        })
                $('select[name="file_yewu_private_select"]').eq(1).change(function(){
                    sleep(200)
                         var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="private_config_file"]').find('select').val()
             var yewu=$('div[name="file_yewu_private"]').find('select').val()
             var jiekou=$('div[name="file_yewu_private"]').eq(1).find('select').val()
             var json_data = $('#json_template_private').html()
             var gen_mulu=$.cookie('genmulu')
                    $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"private_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data,jiekou:jiekou},
                        function (data) {
                            $('#json_template_private').html(data.data_config)
                            $('#json_moban_private').html(data.data_json)

                        }

                    )

                })