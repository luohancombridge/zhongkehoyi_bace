
        $(document).ready(function () {

                             $.ajaxSetup({
            async : false
        });

            $('#table4').find('tbody').find('tr').each(function () {
                if ($(this).is(':visible')) {
                    $(this).attr('shown', 'true')
                }
                     else
            {
                $(this).removeAttr('shown')
            }
            }
            )
        })
            //监听第一个搜索框内容发生改变
        $("#check_1").bind("DOMNodeInserted", function (e) {
            var name = $(this).html()
            $("#check_2").find('a').html('all')
            $('#table4').find('tr:gt(0)').removeAttr('shown')
            $('#table4').find('tr[name="' + name + '"]').attr('shown','true')
            if (name=='all')
            {
                $('#table4').find('tr:gt(0)').attr('shown','true')
            }
        })
        //监听第二个搜索框内容发生改变
        $("#selecttwo").bind("DOMNodeInserted", function (e) {
            name = $(this).find('a').html()
            $('#table4').find('tr:gt(0)').removeAttr('shown')
            if (name!='all') {
                $('#table4').find('tr[class="' + name + '"]').attr('shown','true')
            }
            else
            {
                name=$("#check_1").html()
                $('#table4').find('tr[name="' + name + '"]').attr('shown','true')
            }
        })

        //case 搜索
        function sousuo_fun() {
            var name = $.trim($('#sousuo_name').val())
            $('#table4').find('tbody').find('tr').each(function () {
                if ($(this).attr('shown') == 'true') {
                    if ($(this).attr('class').indexOf(name) >= 0) {
                        $(this).show()
                    } else {
                        $(this).hide()
                    }
                }
            })
        }

        $('#case_sousuo').click(function () {
            sousuo_fun()

        })


        $(document).keyup(function () {
            if (event.keyCode == 13) {
                sousuo_fun()
            }
        })

    //log设置提交给local，创建或者修改linu_log文件
    var $SCRIPT_ROOT = 'http://'+window.location.host
    $('#log_submit').click(function()
    {
        var huanjing=$('#log_change_huanjing').val()
        var yewu=$('#log_file_yewu').val()
        var gen_mulu=all_mulu = $.cookie('genmulu')
        var log_mulu=$('#log_mulu').val()
        var server_url=$('#server_url').val()
        var server_port=$('#server_port').val()
        var server_name=$('#server_name').val()
        var server_password=$('#server_password').val()
        var log_begin_split=$('#log_begin_split').val()
         var log_over_split=$('#log_over_split').val()
        var post_url='http://127.0.0.1'  + ':'+$('[ name="get_port"]').attr('port') + '/linux_log_reserver'
        $.post(post_url,{huanjing:huanjing,yewu:yewu,gen_mulu:gen_mulu,log_mulu:log_mulu,
       ip:server_url, port:server_port,name:server_name,password:server_password,
       log_begin_split:log_begin_split, log_done_split:log_over_split},function(data)
        {
            if (data.statu=="success")
            {
               $('#take_linux_log_kuang') .modal('hide')
                 layer.msg('更新成功', {
                            shade: [0.3, '#fff'],
                            shadeClose: true,
                            icon: 1,
                            time: 2000 //2秒关闭（如果不配置，默认是3秒）
                        })

            }
            else
            {
                $('#take_linux_log_kuang') .modal('hide')
                 layer.msg(data.error, {
                            shade: [0.3, '#fff'],
                            shadeClose: true,
                            icon: 2,
                            time: 2000 //2秒关闭（如果不配置，默认是3秒）
                        })
            }
        })
    })
    //log 配置模态框点击打开，初始化信息
    $('#take_linux_log_kuang').on('shown.bs.modal', function (e) {
      var huanjing=$('#log_change_huanjing').val()
        var yewu=$('#log_file_yewu').val()
        var gen_mulu=all_mulu = $.cookie('genmulu')
        $.post('http://127.0.0.1'  + ':'+$('[ name="get_port"]').attr('port') + '/read_linux_log',
            {huanjing:huanjing,yewu:yewu,gen_mulu:gen_mulu},function(data){
              if (data.statu!='success'){
                        alert("读取信息失败")
              }
              else
              {
                  $.each( data.linux_log_detail,function(a,b)
                  {
                      if (a=="linux")
                      {
                        $.each(b,function(u,z)
                        {
                            if (u=="ip")
                            {
                                $('#server_url').val(z)
                            }
                            else if(u=="port")
                            {
                                 $('#server_port').val(z)
                            }
                             else if(u=="name")
                            {
                                 $('#server_name').val(z)
                            }
                               else if(u=="password")
                            {
                                 $('#server_password').val(z)
                            }
                        })
                      }
                      elif(a=="split_detail")
                      {
                          $.each(b,function(k,z)
                          {
                                if (k=="log_begin_split")
                           {
                                $('#log_begin_split').val(z)
                           }
                           if (k=="log_done_split")
                           {
                                $('#log_over_split').val(z)
                           }

                          })

                      }
                      elif(a=="mulu")
                      {
                           $.each(b,function(k,z)
                           {
                                $('#log_mulu').val(z)
                           }
                           )
                      }
                  })

              }

            })
})
    //点击读取case的go按钮，存储根目录cookie
    $('#submit_url').click(function () {
         $.cookie("genmulu", "", {expires: -1})
        $.cookie('genmulu', $('#mulu_url').val());

    })
    //获取local  server版本信息
    $(document).ready(function(){
    $('[name="chuancan_type"]').hide()
    $('[name="login_info"]').hide()
var ip = $('input[name="ip_dizhi"]').val()
    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1' + ':' + $('[ name="get_port"]').attr('port') + '/banben_data',
        data: "",
        error: function (data, type, err) {
            layer.alert('请启动本地server ,若已启动，请从git库更新代码 http://172.16.101.32/haiyongli/local_server.git', {icon: 2})
        },
        success: function (msg) {
            if (msg.statu != 3) {
                layer.alert('版本过低，请从git库更新代码地址：http://172.16.101.32/haiyongli/local_server.git', {icon: 2})
            }
        }
    })
    })
        //创建接口，环境选择改动，更改业务名
        var local_host = 'http://' + window.location.host
        var ip = $('input[name="ip_dizhi"]').val()
$('#create_change_huanjing').change(function(){
    huanjing=$('#create_change_huanjing').val()
    all_mulu = $.cookie('genmulu')
    ip_dizhi = $('#tag_shuruip').attr('name')
    $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/get_all_jiekou', {mulu: all_mulu, huanjing: huanjing, ip_dizhi: ip_dizhi},
        function (data) {
            $("#create_file_yewu").empty()
            for (var i=0;i<data.all_yewu.length;i++)
            {
               $("#create_file_yewu").append('<option>'+data.all_yewu[i]+'</option>')
            }

        }
    )
})
        //公共配置文件修改弹出框，根据环境显示业务
    $('#publick_config_select_huanjing').change(function(){
    huanjing=$('#publick_config_select_huanjing').val()
    all_mulu = $.cookie('genmulu')
    ip_dizhi = $('#tag_shuruip').attr('name')
    $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/get_all_jiekou', {mulu: all_mulu, huanjing: huanjing, ip_dizhi: ip_dizhi},
        function (data) {
            $("#publick_config_change_yewu_select").empty()
            for (var i=0;i<data.all_yewu.length;i++)
            {

               $("#publick_config_change_yewu_select").append('<option>'+data.all_yewu[i]+'</option>')

            }
        })
            var huanjing=$('div[name="file_secret_publick"]').find('select').val()
             var yewu=$('div[name="file_yewu_publick"]').find('select').val()
             var json_data = $('#json_template_publick').val()
             var gen_mulu=$.cookie('genmulu')

                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"publick_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_publick').val(data.data)
                        }
             )
})
//  接口级配置文件修改
        $('#jiekou_huanjing_change').change(function(){
    huanjing=$('#publick_config_select_huanjing').val()
    all_mulu = $.cookie('genmulu')
    ip_dizhi = $('#tag_shuruip').attr('name')
    $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/get_all_jiekou', {mulu: all_mulu, huanjing: huanjing, ip_dizhi: ip_dizhi},
        function (data) {
            $("#yewu_private_selec_change").empty()
            for (var i=0;i<data.all_yewu.length;i++)
            {
               $("#yewu_private_selec_change").append('<option>'+data.all_yewu[i]+'</option>')
            }
        }
    )
})
    //接口配置文件修改，监控下拉列表业务，如果有发生更改，则更改接口列表
$("#yewu_private_selec_change").change(function(){
        huanjing=$('#publick_config_select_huanjing').val()
    all_mulu = $.cookie('genmulu')
    yewu=$('#yewu_private_selec_change').val()
    ip_dizhi = $('#tag_shuruip').attr('name')
    $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/get_yewu_jiekou', {yewu:yewu,mulu: all_mulu, huanjing: huanjing, ip_dizhi: ip_dizhi},
        function (data) {
            $("#private_select_jjiekou_select").empty()
            for (var i=0;i<data.all_jiekou.length;i++)
            {
               $("#private_select_jjiekou_select").append('<option>'+data.all_jiekou[i]+'</option>')
            }
        })
     $("#private_select_jjiekou_select").find('option').show()
})
//git上传功能，
$('#git_submit_button').click(function()
{
 var mulu=$.trim($('#mulu').next().val())
 var ip = $('input[name="ip_dizhi"]').val()
 if ($.trim(ip)=='')
 {
 ip=window.location.host.split(':')[0]
 }
 var git_address=$.trim($('#git_address').next().val())
 if  (mulu=='' ||  git_address=='' )
 {
 $('#git_submit_alert').html('参数均不能为空')
    $('#git_submit_alert').show()

 }
 else
 {
 var index = layer.load(1, {
  shade: [0.1,'#fff'] //0.1透明度的白色背景
});
$('#git_submit').modal('hide')
     $.post('http://' + '127.0.0.1' + ':'+$('[ name="get_port"]').attr('port') + '/set_local_file_save', {mulu:mulu, git_address: git_address,ip:ip},
        function (data) {
        layer.close(index)
        if (data.statu=='success')
        {
         layer.msg('上传成功',{icon: 1});

        }
                else if  (data.statu=='no file')
        {
        layer.msg('目录地址不存在',{icon: 2});
        }
        else
        {
        alert(data.detail);
        }


        $.post('http://' + '127.0.0.1' + ':'+$('[ name="get_port"]').attr('port') + '/delete_local_file_save',{file_path:data.file_path},function()
        {

        })

        })
        }
}
)

$('#git_submit').on('hidden.bs.modal', function () {
  $('#git_submit_alert').hide()
})

//log 页面输入重置
    $('#log_chongzhi').click(function () {
        $('#log_mulu').val('')
        $('#server_url').val('')
        $('#server_port').val('')
        $('#get_log_name').val('')
        $('#server_port').val('')
        $('#server_name').val('')
        $('#server_password').val('')
        $('#log_begin_split').val('')
        $('#log_over_split').val('')
    })

    //log  模态框点击关闭
    $('[data-dismiss="take_linux_log_kuang"]').click(function () {
            $('#take_linux_log_kuang').modal('hide')
        }
    )
    //log 模态框 选择环境，发送请求
    $('#log_change_huanjing').change(function () {
        var huanjing = $(this).val()
        var first_yewu = ''
        var gen_mulu = $.cookie('genmulu')
        $.post('http://127.0.0.1:' + $('[ name="get_port"]').attr('port') + '/get_all_jiekou', {
                huanjing: huanjing,
                mulu: gen_mulu,
                ip_dizhi: $('input[name="ip_dizhi"]').val()
            },
            function (data) {
                if (data.statu == 'success') {
                    $('#log_file_yewu').empty()
                    var append_htmle = ''
                    first_yewu = data.all_yewu[0]
                    for (var i = 0; i < data.all_yewu.length; i++) {
                        append_htmle = append_htmle + '<option>' + data.all_yewu[i] + '</option>'
                    }
                    $('#log_file_yewu').append(append_htmle)
                }


                $.post('http://127.0.0.1' + ':' + $('[ name="get_port"]').attr('port') + '/raad_log_file', {
                        huanjing: huanjing,
                        mulu: gen_mulu,
                        yewu: first_yewu
                    },
                    function (data) {
                        alert(data.statu)
                        if (data.statu == 'read_success') {
                            var detail = $.parseJSON(data.detail)
                            $('#get_log_name').val(detail.name)
                            $('#log_mulu').val(detail.mulu)
                            $('#server_url').val(detail.ip)
                            $('#server_port').val(detail.port)
                            $('#server_name').val(detail.user)
                            $('#server_password').val(detail.password)
                            $('#log_begin_split').val(detail.begin_str)
                            $('#log_over_split').val(detail.finish_str)
                        }
                    })
            })
    })

//根据页面选择后台加密，登录框显示与否
$('[name="sign_type"]').find('select').change(function(){
if ($(this).val()=='Backstage_web')
{
$('[name="login_info"]').hide()

}
if ($(this).val()!='Backstage_web')
{
$('[name="login_info"]').hide()

}
})
//设置传参方式
$('[name="file_method"]').change(function(){
if ($(this).find('select').val()=='post')
{
$('[name="chuancan_type"]').show()
}
else
{
$('[name="chuancan_type"]').hide()
}

})


        // $('#create_file_save_last').click(function () {
        //     //环境名称
        //     if ($('#basic-url').is(':visible')) {
        //         alert(2222)
        //         var ip = $('input[name="ip_dizhi"]').val()
        //         var huanajing = $('div[name="file_secret"]').find('select').val()
        //         var yewu = $('div[name="file_yewu"]').find('select').val()
        //         var sign_type = $('div[name="sign_type"]').find('select').val()
        //         var oter_publick_url = ''
        //         if (sign_type == '猪博士app') {
        //             oter_publick_url = $('#create_jiekou_publick_url_save').find('option:selected').attr('publick_url_num')
        //         }
        //         var method = $('div[name="file_method"]').find('select').val()
        //         var request_url = $('#basic-url').val()
        //         var json_data = $('#json_template').val()
        //         $('#publick_db').modal('hide')
        //         if ($('#file_jiekou_name').val().indexOf(" ") >= 0) {
        //             alert("接口名不能包含空格")
        //         } else {
        //
        //             $.post('http://' + ip + ':' + $('[ name="get_port"]').attr('port') + '/creat_file', {
        //                     gen_mulu: $.cookie('genmulu'),
        //                     oter_publick_url: oter_publick_url,
        //                     yewu: yewu,
        //                     huanjing: huanajing,
        //                     sign_type: sign_type,
        //                     request_type: $('[name="send_request"]').find('select').val(),
        //                     method: method,
        //                     request_url: request_url,
        //                     json_data: json_data,
        //                     jiekou_name: $('#file_jiekou_name').val()
        //                 },
        //                 function (data) {
        //                     if (data.statu == "success") {
        //                         layer.msg('创建成功', {icon: '1'})
        //                     } else {
        //                         layer.msg(data.statu, {icon: '0'})
        //                     }
        //                 }
        //             )
        //
        //         }
        //     }
        //
        //
        //     //保存db配置文件
        //     if ($('#json_template_db').is(':visible')) {
        //         alert(3333)
        //         var ip = $('input[name="ip_dizhi"]').val()
        //         var huanjing = $('div[name="file_secret_db"]').find('select').val()
        //         var yewu = $('div[name="file_yewu_db"]').find('select').val()
        //         var json_data = $('#json_template_db').val()
        //         var gen_mulu = $.cookie('genmulu')
        //         var json_data = $('#json_template_db').val()
        //         $('#publick_db').modal('hide')
        //         $.post('http://' + ip + ':' + $('[ name="get_port"]').attr('port') + '/save_conifg', {
        //                 type: "db_config",
        //                 gen_mulu: gen_mulu,
        //                 yewu: yewu,
        //                 huanjing: huanjing,
        //                 json_data: json_data,
        //             },
        //             function (data) {
        //                 if (data.statu == "success") {
        //                     layer.msg('更新成功', {icon: '1'})
        //
        //                 } else {
        //                     layer.msg(data.statu, {icon: '0'})
        //                 }
        //             }
        //         )
        //     }
        //
        //
        //     //保存publick配置文件
        //     if ($('#json_template_publick').is(':visible')) {
        //         alert(444444)
        //         var ip = $('input[name="ip_dizhi"]').val()
        //         var huanjing = $('div[name="file_secret_publick"]').find('select').val()
        //         var yewu = $('div[name="file_yewu_publick"]').find('select').val()
        //         var json_data = $('#json_template_publick').val()
        //         var gen_mulu = $.cookie('genmulu')
        //
        //         $('#publick_db').modal('hide')
        //         $.post('http://' + ip + ':' + $('[ name="get_port"]').attr('port') + '/save_conifg', {
        //                 type: "publick_config",
        //                 gen_mulu: gen_mulu,
        //                 yewu: yewu,
        //                 huanjing: huanjing,
        //                 json_data: json_data,
        //             },
        //             function (data) {
        //                 if (data.statu == "success") {
        //                     layer.msg('更新成功', {icon: '1'})
        //
        //                 } else {
        //                     layer.msg(data.statu, {icon: '0'})
        //                 }
        //             }
        //         )
        //     }
        //
        //     //保存接口配置配置文件
        //     if ($('select[name="file_yewu_private_select"]').is(':visible')) {
        //         alert(55555)
        //         var ip = $('input[name="ip_dizhi"]').val()
        //         var huanjing = $('div[name="file_secret_publick"]').find('select').val()
        //         var yewu = $('div[name="file_yewu_private"]').find('select').val()
        //         var jiekou = $('#private_select_jjiekou_select').val()
        //         var config_data = $('#json_template_private').val()
        //         var gen_mulu = $.cookie('genmulu')
        //         var json_text = $('#json_moban_private').val()
        //         $('#publick_db').modal('hide')
        //         $.post('http://' + ip + ':' + $('[ name="get_port"]').attr('port') + '/save_conifg', {
        //                 type: "private_config",
        //                 gen_mulu: gen_mulu,
        //                 huanjing: huanjing,
        //                 yewu: yewu,
        //                 config_data: config_data,
        //                 json_data: json_text,
        //                 jiekou: jiekou
        //
        //             },
        //             function (data) {
        //                 if (data.statu == "success") {
        //                     layer.msg('更新成功', {icon: '1'})
        //
        //                 } else {
        //                     layer.msg(data.statu, {icon: '0'})
        //                 }
        //
        //             }
        //         )
        //     }
        // })

    //初始化目录
    // $('#create_file_save_last').click(function()
    // {
    //     if ($('[href="#create_file"]').attr('aria-expanded')=='true')
    //     {
    //         var sign_type=$('#create_file_type').val()
    //         var muluming=$('#muluming').val()
    //          var yewuming=$('#yewuming').val()
    //          var gongnengming=$('#gongnengming').val()
    //          var publick_url=$('#publick_url').val()
    //          if ($('#create_file_name_pass').is(':visible'))
    //          {
    //             var name=$('#file_login-name').val()
    //               var password=$('#file_login-password').val()
    //          }
    //          else
    //          {
    //               var name=''
    //               var password=''
    //          }
    //                  if ( $('#opend_api_create').is(':visible'))
    //          {
    //            var token_url= $('#token_url').val()
    //                var user_name= $('#name').val()
    //                var password= $('#password').val()
    //                var Verification_code= $('#Verification_code').val()
    //          }
    //                  else
    //                  {
    //                      var token_url=''
    //                var client_id= ''
    //                var client_secret= ''
    //                var grant_type= ''
    //                  }
    //
    //
    //                                    if ( $('#yunfuw_all').is(':visible'))
    //          {
    //                var name= $('#yunfuw_name').val()
    //                var password= $('#yunfuw_password').val()
    //          }
    //         if ($('#alpha_create').is(':visible')) {
    //             var name = $('#alpha_name').val()
    //             var password = $('#alpha_password').val()
    //         }
    //         if ($('#b_duan_session').is(':visible')) {
    //             var name = $('#b_duan_sess').val()
    //             var password = $('#b_duan_user').val()
    //             var session_id=''
    //         }
    //                    if ($('#pig_cocter_create_all').is(':visible')) {
    //             var name =$('#pig_cocter_create_all').find('#name').val()
    //                        var password = $('#pig_cocter_create_all').find('#password').val()
    //                        var Verification_code = $('#pig_cocter_create_all').find('#Verification_code').val()
    //                        publick_url = []
    //                        $('#more_top_publick_url').find('input').each(function () {
    //
    //                            publick_url.push($(this).val())
    //                        })
    //                        publick_url = JSON.stringify(publick_url)
    //
    //                    }
    //         $.post('http://127.0.0.1:' + $('[ name="get_port"]').attr('port') + '/new/create_new_file', {
    //             session_id:session_id,user_name:user_name,password:password,Verification_code:Verification_code,sign_type:sign_type,name:name,muluming: muluming, yewuming: yewuming, gongnengming: gongnengming, publick_url: publick_url
    //         }, function (data) {
    //             if (data.statu == 'success') {
    //                   $('#publick_db').modal('hide')
    //                 layer.msg('创建成功', {
    //                     shade: [0.3, '#fff'],
    //                     shadeClose: true,
    //                     icon: 1,
    //                     time: 2000 //2秒关闭（如果不配置，默认是3秒）
    //                 })
    //             } else {
    //                 $('#publick_db').modal('hide')
    //                 $('#muluming').val('')
    //                 $('#yewuming').val('')
    //                 $('#gongnengming').val('')
    //                 $('#publick_url').val('')
    //                 layer.msg(data.statu, {
    //                     shade: [0.3, '#fff'],
    //                     shadeClose: true,
    //                     icon: 2,
    //                     time: 2000 //2秒关闭（如果不配置，默认是3秒）
    //                 })
    //             }
    //         })
    //     }
    // })







$('#submit_url').click(function(){
    $.ajaxSetup({
            async : false
        });
       var mulu=$('#mulu_url').val()
    $.cookie('mulu_detail',mulu)
       var  huanjing=''
    var detail=''
     var all_data=''
            $.post('http://127.0.0.1:' + $('[ name="get_port"]').attr('port') + '/mulu_detail', {
            mulu:mulu,huanjing:huanjing
            }, function (data) {
             all_data=JSON.stringify(data)
                         $.post($SCRIPT_ROOT + '/uplate_jiekou_list', {
                       mulu:mulu,detail:detail,local_ip:'10.4.148.206',all_data:all_data
                    },
                    function (data) {
                       window.location.reload()

                    }
                )
            }
            )

})




        $("#check_0").bind("DOMNodeInserted", function (e) {
               $.ajaxSetup({
            async : false
        });
            huanjing = $(this).html()
            all_mulu = $.cookie('genmulu')
            ip_dizhi = $('#tag_shuruip').attr('name')
                var  detail=''
         $.post('http://127.0.0.1:' + $('[ name="get_port"]').attr('port') + '/new/new_mkulu_detail', {
            mulu:all_mulu,huanjing:huanjing
            }, function (data) {
            detail=data.data
            }
            )
            $.post($SCRIPT_ROOT + '/uplate_jiekou_list', {mulu: all_mulu, huanjing: huanjing, ip_dizhi: ip_dizhi,detail:detail},
                function (data) {
                }
            )
            window.location.reload()
        })






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

                                       $.ajaxSetup({
            async : true
        })
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
                    var  return_data=''
                var ip_dizhi = $('#tag_shuruip').attr('name')
                $.post($SCRIPT_ROOT + '/piliang_run', {
                        all_jiekou_re: all_mulu,
                        huanjing: huanjing,
                        gen_mulu: gen_mulu,
                        ip_dizhi: window.location.host,
                    local_ip:$('input[name="ip_dizhi"]').val()
                    },
                    function (data) {
                       return_data=data.return_data
                       let post_url='http://127.0.0.1'  + ':'+$('[ name="get_port"]').attr('port') + '/piliang_run'
                        $.post(post_url,{data:return_data},function(data)
                        {

                        })
                    }
                )
            check_statu = setInterval("run_statu()",1000);
                }
            }
        )
        //单个接口跑
        $('button[name="simple_run_list"]').click(function () {

                                          $.ajaxSetup({
            async : true
        })
                $('#run_result_open').html('运行中')
            $('#run_result_open').attr('disabled',true)
                var all_mulu = []
                all_mulu.push($(this).parent().parent().find('td>input').attr('class'))
                var all_mulu = JSON.stringify({'all_mulu': all_mulu})
                var huanjing = $('#check_0').html()
                var gen_mulu = $.cookie('genmulu')
                var ip_dizhi = $('#tag_shuruip').attr('name')
            var return_data=''
                layer.msg('开始运行', {icon: '1'})
                $.post($SCRIPT_ROOT + '/piliang_run', {
                        all_jiekou_re: all_mulu,
                        huanjing: huanjing,
                        gen_mulu: gen_mulu,
                        ip_dizhi: window.location.host,
                    local_ip:$('input[name="ip_dizhi"]').val()
                    },
                    function (data) {
                                return_data=data.return_data
                       let post_url='http://127.0.0.1'  + ':'+$('[ name="get_port"]').attr('port') + '/piliang_run'
                        $.post(post_url,{data:return_data},function(data)
                        {

                        })
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
        // $('button[name="tiaoshi_tiaozhuan"]').each(function () {
        //     $(this).click(function () {
        //             mulu = $(this).find('span').attr('name')
        //             var huanjing = $('#check_0').html()
        //             var gen_mulu = $.cookie('genmulu')
        //             $.post($SCRIPT_ROOT + '/jiekou_mulu', {mulu: mulu, statu: "调试", huanjing: huanjing, gen_mulu: gen_mulu},
        //                 function (data) {
        //                     $.post('http://127.0.0.1:' + $('[ name="get_port"]').attr('port')  + '/jiankong_mulu', {
        //                             mulu: mulu
        //                         },
        //                         function (data) {
        //                             window.location.replace($SCRIPT_ROOT + '/shishitiaoshi')
        //                         }
        //                     )
        //                 }
        //             )
        //         }
        //     )
        // })
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
             var json_data = $('#json_template_publick').val()
             var gen_mulu=$.cookie('genmulu')
                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"publick_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_publick').val(data.data)

                        }

             )


        })


                $('select[name="publick_config_change"]').bind("change",function () {
                    sleep(200)
                                 var ip = $('input[name="ip_dizhi"]').val()
            var huanjing=$('div[name="file_secret_publick"]').find('select').val()
             var yewu=$('div[name="file_yewu_publick"]').find('select').val()
             var json_data = $('#json_template_publick').val()
             var gen_mulu=$.cookie('genmulu')
                 $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"publick_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_publick').val(data.data)

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
                           $('#json_moban_private').text(data.data_json)
                            $('#json_template_private').val(data.data_config)
                            $("#private_select_jjiekou_select").empty()
                            for (var i=0;i<data.jiekou_list.length;i++)
                            {

                                $("#private_select_jjiekou_select").append('<option>'+data.jiekou_list[i]+'</option>')

                            }
                        }
             )
        })
                $('select[name="private_config_change"]').bind("change",function () {
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
        var json_data = $('#json_template_db').val()
         var gen_mulu=$.cookie('genmulu')
                $.post('http://' + ip + ':'+$('[ name="get_port"]').attr('port') + '/read_config', {type:"db_config",gen_mulu:gen_mulu,huanjing:huanjing,yewu:yewu,json_data:json_data},
                        function (data) {
                               $('#json_template_db').val(data.data)
                        }
             )
})
        $('select[name="db_config_change"]').bind("change", function () {
            sleep(200)
            var ip = $('input[name="ip_dizhi"]').val()
            var huanjing = $('div[name="file_secret_db"]').find('select').val()
            var yewu = $('div[name="file_yewu_db"]').find('select').val()
            var json_data = $('#json_template_db').val()
            var gen_mulu = $.cookie('genmulu')
            $.post('http://' + ip + ':' + $('[ name="get_port"]').attr('port') + '/read_config', {
                    type: "db_config",
                    gen_mulu: gen_mulu,
                    huanjing: huanjing,
                    yewu: yewu,
                    json_data: json_data
                },
                function (data) {
                    $('#json_template_db').val(data.data)
                }
            )
        })
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
