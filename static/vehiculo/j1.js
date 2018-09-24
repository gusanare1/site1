        function getCiudades() {
            var ProvinciaId = $("#id_provincia").val();
            if (ProvinciaId) {
                // Eliminamos las opciones anteriores del select
                $ciudades=$("#id_ciudad").html();
                var request = $.ajax({
                    type: "GET",
                    url: "{% url 'get_ciudades' %}",
                    data: {
                        "provincia_id": ProvinciaId,
                    },
                });
                request.done(function(response) {
                    // Agregamos los resultados al select
                    $("#id_ciudad").html(response.ciudades);
                    
                });
            } else {
                $("#id_ciudad").html("");
                }
        }    
			
        function getModelos() {
            var marcaId = $("#id_marca").val();
            if (marcaId) {
                $("#id_modelo").html("");
                var request = $.ajax({
                    type: "GET",
                    url: "{% url 'get_modelos' %}",
                    data: {
                        "marca_id": marcaId,
                    },
                });
                request.done(function(response) {
                    // Agregamos los resultados al select
                    $("#id_modelo").html(response.modelos);
                    
                });
            } else {
                $("#id_modelo").html("");
                }
        }

   