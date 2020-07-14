var base_url="";

function post_ajax_data(api_name, encodedata, success)
{
   var url = base_url + api_name;

   $.ajax({
      type:"POST",
      url:url,
      data:encodedata,
      dataType:"json",
      restful:true,
      cache:false,
      timeout:80000,
      async:true,
      success:function(data){
         success.call(this, data);
      },
      error:function(data){
         alert("connect failed");
      }
   });
}

function get_ajax_data(api_name, success)
{
   var url = base_url + api_name;

   $.ajax({
      type:"GET",
      url:url,
      dataType:"json",
      restful:true,
      cache:false,
      timeout:20000,
      async:true,
      success:function(data){
         success.call(this, data);
      },
      error:function(data){
         alert("connect failed");
      }
   });
}

function put_ajax_data(api_name, encodedata, success)
{
   var url = base_url + api_name;

   $.ajax({
      type:"PUT",
      url:url,
      data:encodedata,
      dataType:"json",
      restful:true,
      cache:false,
      timeout:20000,
      async:true,
      success:function(data){
         success.call(this, data);
      },
      error:function(data){
         alert("connect failed");
      }
   });
}

function delete_ajax_data(api_name, success)
{
   var url = base_url + api_name;

   $.ajax({
      type:"DELETE",
      url:url,
      dataType:"json",
      restful:true,
      cache:false,
      timeout:20000,
      async:true,
      success:function(data){
         success.call(this, data);
      },
      error:function(data){
         alert("connect failed");
      }
   });
}
