//第一个为分页最外面ul的定位器，第二个为列表body的定位器，第三个参数为每个一页多少行
//分页初始化，只针对显示的列表元素
function  fenye_def(a,b,num)
{
    if (num==0)
    {
        //获取当前屏幕高度
        var chushi_length=0
        var screen_height=window.screen.height
        //遍历列表，从上到下查看哪行数据的位置在最下面差距20，即为num的值
        b.find('tr').each(function(k,d)
        {
            var thia_height=$(this).offset().top
            if   (screen_height-thia_height<80  && num==0 )
            {
                num=k+1
            }
        })
    }
    //初始化分页元素
    var li_length=a.find('li').length
    a.find('li').each(function(k,z)
    {
        if (k!=0 && k !=li_length-1)
        {
           $(this).remove()
        }
    })
    a.attr('this_yema','1')
    var statu=0
    var all_li= a.find('li')
b.find('tr').each(function(a,b){
    if (!$(this).is(':hidden')   ||  $(this).attr('fenye_row')!="undefined")
    {
      $(this).attr('fenye_row',parseInt(a/num+1))
        if (parseInt(a/num+1)>1)
        {
            $(this).hide()
        }
    if (parseInt(a/num+1)!=statu)
    {
        statu=parseInt(a/num+1)
        all_li .eq(-1).before('<li  ><a href="#">'+String(parseInt(a/num+1))+'</a></li>')
    }
    }
})

    click_shwo(a,b)
}
//点击按钮
function  click_shwo(el,table_el)
{
        el.on('click','li',function()
    {
        if ($(this).find('a').html()=='»')
        {
        var max_fenye= parseInt($('.pagination').find('li').eq(-2).find('a').html())
            if ($('.pagination').attr('this_yema')!=String(max_fenye))
            {
                $('.pagination').find('.active').next().attr('class','active')
                $('.pagination').find('.active').eq(0).removeAttr('class')
                var this_ye= parseInt($('.pagination').find('.active').find('a').html())
                $('.pagination').attr('this_yema',this_ye)

            }
        }
        else if($(this).find('a').html()=='«')
            {
                if ($('.pagination').attr('this_yema')!='1')
        {
            $('.pagination').find('.active').prev().attr('class','active')
            $('.pagination').find('.active').eq(-1).removeAttr('class')
            var this_ye= parseInt($('.pagination').find('.active').find('a').html())
            $('.pagination').attr('this_yema',this_ye)

        }
    }
        else {
            $('.pagination').find('li').removeAttr('class')
            $('.pagination').attr('this_yema',  $(this).find('a').html())
            $(this).attr('class','active')
        }
        var thies_row= $('.pagination').find('.active').find('a').html()
        table_el.find('tr').each(function()
        {
            if ($(this).attr('fenye_row')==thies_row)
            {
                $(this).show()
            }
            else
            {
                $(this).hide()
            }
        })
    })

}

//全选选择框必须属性name="all_choice"
$('[name="all_choice"]').click(function()
{
    if ($(this).is(':checked'))
    {
        $(this).parents('table').find('tbody').find('tr[fenye_row]').each(function()
        {

            $(this).find('[type="checkbox"]').attr('checked',true)
        })
    }
    else
    {

        $(this).parents('table').find('tbody').find('tr[fenye_row]').each(function()
        {
            $(this).find('[type="checkbox"]').attr('checked',false)
        })
    }
})


