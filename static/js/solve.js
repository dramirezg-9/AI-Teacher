// historial que se enviará
history = {'work':'work'}
//cuenta las ecuaciones que hay
count = 0
    function deleteEquation(num){
        //se obtienen los elementos a eliminarse
        var eq = document.getElementById('eq'+num.toString());
        var cn = document.getElementById('cn'+num.toString());
        var deleter = document.getElementById('deleter'+num.toString());
        var mover = document.getElementById('mover'+num.toString());
        var letter = '';

        //manipulación del historial
        if (cn.innerHTML){
            letter = cn.innerHTML.charAt(0);
            var pos = cn.innerHTML.slice(1,-1);
            history[letter].splice(pos, 1);
        }
        history['main'].splice(num, 1);

        //se eliminan
        eq.parentNode.removeChild(eq);
        cn.parentNode.removeChild(cn);
        deleter.parentNode.removeChild(deleter);
        mover.parentNode.removeChild(mover);

        // se actualizan el resto de elementos
        for (var i = num+1; i < count; i++){
            x = document.getElementById("cn"+i.toString());
            if (x.innerHTML && x.innerHTML.charAt(0)==letter){
                newnum = parseInt(x.innerHTML.slice(1,-1))-1;
                x.innerHTML = 'E' + newnum.toString() + ":";
                history[letter][newnum] = history[letter][newnum] - 1;
            }
            j = i-1;
            x.id = "cn"+j.toString();
            document.getElementById("eq"+i.toString()).id = "eq"+j.toString();
            document.getElementById("deleter"+i.toString()).id = "deleter"+j.toString();
            document.getElementById("mover"+i.toString()).id = "mover"+j.toString();
        }
        count--;
    }

    function addToHistory(){
        //inicialización de variables importantes
        var equation = document.getElementById("equation_editor").value
        var cont = true
        var part1 = ''
        var part2 = ''
        var num = '0'

        if (equation.indexOf(':') == 1){
            //si la ecuación tiene identificación
            letter = equation.charAt(0);

            var pos = 0
            part2 = equation.slice(2);
            if('main' in history){
                pos = Object.keys(history['main']).length;
                history['main'].push(part2);
            } else{
                history['main'] = [part2];
            }
            if(letter in history){
                num = Object.keys(history[letter]).length.toString();
                history[letter].push(pos);
            } else{
                history[letter] = [pos];
            }
            part1 = letter + num + ':';
        } else{
            //si no la tiene
            part1 = '';
            part2 = equation;
            if('main' in history){
                history['main'].push(equation);
            } else{
                history['main'] = [equation];
            }
        }
        // se añaden los elementos
        if (cont){
            var parent = document.getElementById("history");
            parent.appendChild(createMover("main", count));
            parent.appendChild(createCounter("main", count, part1));
            parent.appendChild(createEquation("main", count, part2));
            parent.appendChild(createDeleter("main", count));
            count ++;
            document.getElementById('equation_editor').value = "";
        }
    }

    //cambio de visibilidad de la historia
    function toggleVisibility(){
        if (document.getElementById("history").style.display == "none"){
            document.getElementById("history").style.display="grid"
        }else{
            document.getElementById("history").style.display="none"
        }
    }
    
    // arrastrar la ecuación
    function dragBars(e){
        // se inicializan el número de la ecuación y el movible
        console.log(history['main'])
        var num = 0;
        var mover = null;
        if(e.target.id){
            num = parseInt(e.target.id.toString().slice(5));
            mover = e.target;
        }else{
            num = parseInt(e.target.parentNode.id.toString().slice(5));
            mover = e.target.parentNode;
        }
        
        // se inicializa el rectángulo de mover
        var posmover = mover.getBoundingClientRect();

        // se hace invisible la ecuación
        mover.style.display = 'none';
        var eq = document.getElementById('eq'+num.toString());
        eq.style.display = 'none';
        var cn = document.getElementById('cn'+num.toString());
        cn.style.display = 'none';
        var deleter = document.getElementById('deleter'+num.toString());
        deleter.style.display = 'none';

        //se consigue el elemento main y el rectángulo de main
        var main = document.getElementsByTagName('main')[0];
        var posmain = main.getBoundingClientRect();

        //se crea el fantasma y se añade a main
        var phantom = createPhantom(num);
        main.appendChild(phantom);

        //se define la posición del fantasma
        var temp = posmover.left-20 - posmain.left
        phantom.style.left = temp.toString()+'px';
        temp = posmover.top -10 - posmain.top
        phantom.style.top = temp.toString()+'px';

        //se añade la línea verde
        var eqHistory = mover.parentNode
        var line = document.createElement('div')
        line.className = 'line'
        eqHistory.insertBefore(line, mover);

        //el número donde al final quedará la ecuación arrastrada
        var lastI = num;

        // código para hacer el fantasma arrastable
        // funcion cuando se mueve el mouse
        document.onmousemove = function(e){
            var newY = parseInt(phantom.style.top.slice(0,-2)) + e.movementY;
            phantom.style.top = newY.toString()+"px";
            for (var i = 0; i < count; i++){
                if (i != num){
                    var checkBox = document.getElementById('mover'+i.toString()).getBoundingClientRect();
                    var relY = e.clientY - checkBox.top;
                    if (0 <= relY && relY<= (checkBox.height/2)){
                        if (i-1 != lastI && i-1 >= num){
                            lastI = i-1;
                            line = line.parentNode.removeChild(line);
                            eqHistory.insertBefore(line, document.getElementById('mover'+i.toString()));
                        } else if(i != lastI && i < num){
                            lastI = i;
                            line = line.parentNode.removeChild(line);
                            eqHistory.insertBefore(line, document.getElementById('mover'+i.toString()));
                        }
                        break;
                    } else if (checkBox.height/2 <= relY && relY < checkBox.height + 10){
                        if (i+1 != lastI && i+1<=num){
                            lastI = i+1;
                            line = line.parentNode.removeChild(line);
                            eqHistory.insertBefore(line, document.getElementById('mover'+lastI.toString()))
                        } else if(i != lastI && i > num){
                            lastI = i;
                            var tempI= i+1;
                            line = line.parentNode.removeChild(line);
                            eqHistory.insertBefore(line, document.getElementById('mover'+tempI.toString()));
                        }
                        break;
                    }
                }
            }
        };

        // funcion cuando se levanta el mouse
        document.onmouseup = function(e){
            console.log(history)
            // remover todos los elementos temporales
            phantom.parentNode.removeChild(phantom);
            document.onmousemove = null;
            document.onmouseup = null;

            // quitar las anteriores ids
            mover.id = null
            eq.id = null
            cn.id = null
            deleter.id = null

            // quitar los elementos de la historia, pero mantenerlos en el documento
            mover = eqHistory.removeChild(mover)
            eq = eqHistory.removeChild(eq)
            cn = eqHistory.removeChild(cn)
            deleter = eqHistory.removeChild(deleter)

            // si tiene letra, y la posición dentro de la letra
            var letter = '';
            var pos = -1;
            if (cn.innerHTML){
                letter = cn.innerHTML.charAt(0);
                pos = parseInt(cn.innerHTML.slice(1,-1));
                history[letter].splice(pos, 1);
            }
            history['main'].splice(num, 1)

            var replace = pos;

            // ciclos de actualización de ids y de historia
            if (lastI > num){
                for (var i = num+1; i <= lastI; i++){
                    var x = document.getElementById("cn"+i.toString())
                    var j = i-1;
                    x.id = "cn"+j.toString();
                    document.getElementById("eq"+i.toString()).id = "eq"+j.toString();
                    document.getElementById("deleter"+i.toString()).id = "deleter"+j.toString();
                    document.getElementById("mover"+i.toString()).id = "mover"+j.toString();
                    if (x.innerHTML && x.innerHTML.charAt(0) == letter){
                        replace = parseInt(x.innerHTML.slice(1,-1))
                        var newnum = replace-1;
                        x.innerHTML = letter + newnum.toString() + ":";
                        history[letter][newnum] = j;
                    }
                }
            } else if (lastI < num){
                for (var i = num-1; i >=lastI; i--){
                    var x = document.getElementById("cn"+i.toString());
                    var j = i+1;
                    x.id = "cn"+j.toString();
                    document.getElementById("eq"+i.toString()).id = "eq"+j.toString();
                    document.getElementById("deleter"+i.toString()).id = "deleter"+j.toString();
                    document.getElementById("mover"+i.toString()).id = "mover"+j.toString();
                    if (x.innerHTML && x.innerHTML.charAt(0) == letter){
                        replace = parseInt(x.innerHTML.slice(1,-1))
                        var newnum = replace+1;
                        x.innerHTML = letter + newnum.toString() + ":";
                        history[letter][replace] = j;
                        console.log(newnum,j);
                    }
                }
            }

            // si tiene letra se reañade a la historia
            if (letter){
                history[letter].splice(replace, 0, lastI);
                cn.innerHTML = letter+replace.toString()+":";
            }

            // cambio de ids de los objetos originales
            mover.id = "mover"+lastI.toString();
            cn.id = "cn"+lastI.toString();
            eq.id = "eq"+lastI.toString();
            deleter.id = "deleter"+lastI.toString();
            history['main'].splice(lastI, 0, eq.innerHTML)

            // se reinsertan y se quita la linea verde
            eqHistory.insertBefore(mover, line);
            eqHistory.insertBefore(cn, line);
            eqHistory.insertBefore(eq, line);
            eqHistory.insertBefore(deleter, line);
            eqHistory.removeChild(line);

            // se hacen visibles
            mover.style.display = 'inline';
            cn.style.display = 'inline';
            eq.style.display = 'inline';
            deleter.style.display = 'inline';
            console.log(history)
        };
    }
    
    // CREAR ELEMENTOS DEL HISTORIAL Y ELEMENTO FANTASMA

    function createPhantom(num){
        var phantom = document.createElement('div');
        phantom.id = 'phantom';
        phantom.appendChild(createMover("phantom", num));
        phantom.appendChild(createCounter("phantom", num, ''));
        phantom.appendChild(createEquation("phantom", num, ''));
        phantom.appendChild(createDeleter("phantom", num));
        return phantom;
    }

    function createDeleter(mode, num){
        var deleter = document.createElement('div');
        deleter.className = 'deleter';
        var circle = document.createElement('i');
        circle.className = 'fas fa-minus-circle';
        deleter.appendChild(circle);
        if (mode != 'phantom'){
            deleter.id = 'deleter'+num.toString();
        }
        deleter.addEventListener("click", function(e){
            if (e.target.id){
                deleteEquation(parseInt(e.target.id.toString().slice(7)))
            }else{
                deleteEquation(parseInt(e.target.parentNode.id.toString().slice(7)))
            }
        })
        return deleter;
    }

    function createMover(mode, num){
        var mover = document.createElement('div');
        mover.className = 'mover';
        var bars = document.createElement('i');
        bars.className = 'fas fa-bars';
        mover.appendChild(bars)
        if (mode != 'phantom'){
            mover.id = 'mover'+num.toString();
        }
        mover.addEventListener("mousedown", function(e){
            dragBars(e);
        })
        return mover;
    }

    function createCounter(mode, num, text){
        var cn = document.createElement('div');
        cn.className = 'counter';
        if (mode == "phantom"){
            var original = document.getElementById('cn'+num.toString());
            cn.appendChild(document.createTextNode(original.innerHTML));
        } else {
            cn.id = 'cn'+num.toString();
            cn.appendChild(document.createTextNode(text));
        }
        return cn;
    }

    function createEquation(mode, num, text){
        var eq = document.createElement('div');
        eq.className = 'equation';
        if (mode == 'phantom'){
            var original = document.getElementById('eq'+num.toString());
            eq.appendChild(document.createTextNode(original.innerHTML));
        } else{
            eq.appendChild(document.createTextNode(text));
            eq.id = 'eq'+num.toString();
        }
        return eq;
    }

    // AJAX PARA SUBIR SOLUCIÓN

    function submitExercise(){
        $.ajax({
            headers: { "X-CSRFToken": $.cookie("csrftoken")},
            url: '/grade/',
            type: 'POST',
            data: {
                'history': JSON.stringify(history)
            },
            success: function(response){
                loadCorrection(response);
            },
            error: function(jqXHR, state, error){
                console.log(state)
                console.log(error)
                console.log(jqXHR.responseText)
            }
        });
    }

    function loadCorrection(response){
        // vaciar calificación anterior
        var correction = document.getElementById('correction');
        while(correction.firstChild){
            correction.removeChild(correction.firstChild);
        }

        // añadir título
        var title_correction = document.createElement('div');
        title_correction.className = 'correction-title';
        title_correction.appendChild(document.createTextNode('Evaluación'));
        correction.appendChild(title_correction);

        // añadir mensaje de calificación
        if (response.error == -1){
            var correct = document.createElement('div');
            correct.appendChild(document.createTextNode('¡Todo fue correcto!'));
            correct.className = 'correcto';
            correction.appendChild(correct);
        } else{
            var num = response.error;
            var incounter = document.createElement('p');
            incounter.appendChild(document.createTextNode(num.toString()));
            var counter = document.createElement('div');
            counter.appendChild(incounter);
            counter.className = 'counter';
            correction.appendChild(counter);
            var equation = document.createTextNode(document.getElementById('eq'+num.toString()).innerHTML);
            var point = document.createElement('div');
            point.className = 'equation';
            point.appendChild(equation);
            correction.appendChild(point)
        }
    }

    // código inicial
    document.getElementsByTagName('main')[0].style.marginBottom = document.getElementsByClassName('page-footer')[0].getBoundingClientRect().height.toString() + 'px'
    document.getElementById("history-btn").addEventListener("click", toggleVisibility)
    document.getElementById("add-btn").addEventListener("click", addToHistory)
    document.getElementById("submit-btn").addEventListener("click", submitExercise)
    window.onresize = function(){
        document.getElementsByName('main')[0].style.marginBottom = document.getElementsByClassName('page-footer')[0].getBoundingClientRect().height.toString() + 'px'
    }