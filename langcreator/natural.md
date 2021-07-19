# assignment

`#name = #value`

    #name = #value
    set #name to #value
    let #name to be #value
    #name is #value
    define #name as #value
    #name := #value
    initialize #name as #value

# update

`#name += #num_or_var`

    #name += #num_or_var
    add #num_or_var to #name

`#name -= #num_or_var`

    #name -= #num_or_var
    subtract #num_or_var from #name

`#name *= #num_or_var`

    #name *= #num_or_var
    multiply #num_or_var by #name

`#name /= #num_or_var`

    #name /= #num_or_var
    divide #num_or_var by #name

`#name **= #num_or_var`

    raise #name to the power of #num_or_var

`#name **= 2`

    square #name

`#name += 1`

    #name++
    increment #name

`#name += #int`

    increment #name by #int

# function

`def #name(#params):`

    def #name #params
    define function #name #params
    let function #name #params
    create function #name #params
    function #name #params
    fun #name #params
    fn #name #params
    subroutine #name #params
    sub #name #params

# operation

`#num_or_var + #num_or_var`

    #num_or_var + #num_or_var
    sum #num_or_var and #num_or_var
    add #num_or_var plus #num_or_var
    #num_or_var plus #num_or_var

`#string_or_var + #string_or_var`

    #string_or_var + #string_or_var
    concatenate #string_or_var and #string_or_var
    join #string_or_var and #string_or_var

`#num_or_var - #num_or_var`

    #num_or_var - #num_or_var
    #num_or_var minus #num_or_var
    difference between #num_or_var and #num_or_var

`#num_or_var * #num_or_var`

    #num_or_var * #num_or_var
    #num_or_var times #num_or_var
    #num_or_var multiplied by #num_or_var

`#num_or_var / #num_or_var`

    #num_or_var / #num_or_var
    #num_or_var divided by #num_or_var

`#num_or_var ** #num_or_var`

    #num_or_var ** #num_or_var
    #num_or_var ^ #num_or_var
    #num_or_var to the power of #num_or_var

`#num_or_var ** 2`

    #num_or_var squared

# list_processing

`[ x[#name] for x in #list_or_var ]`

    select #name from #list_or_var
    from #list_or_var map #name
    #list_or_var.map(#name' => #name'[#name])

`[ x[#name] for x in previous ]`

    map #name
    |> map #name

`[ x for x in previous if #comparison ]`

    filter #comparison
    |> filter #comparison
    grep #comparison

`[ x[#name] for x in #list_or_var if #comparison ]`

    select #name from #list_or_var where #comparison

# call_function

`#name(#args)`

    #name #args
    call #name with #args

`#name()`

    #name()
    call #name

# lambdas

`#name = lambda #params: #expression`

    #name #params = #expression
    #name = lambda #params: #expression
    #name = #params => #expression
    #name = \#params -> #expression

# if

`if #condition:`

    if #condition

`if not #condition:`

    if not #condition
    unless #condition

`if #condition:\n\t#expression_or_statement`

    #expression_or_statement if #condition

`#assignment if #condition else #value`

    #assignment if #condition else #value

`if #condition:\n\t#expression_or_statement\nelse:\n\t#expression_or_statement`

    #expression_or_statement if #condition else #expression_or_statement

# loop

`for #name in #list_or_var:`

    for #name in #list_or_var
    each #name in #list_or_var

`for #name in #list_or_var:\n\t#expression_or_statement`

    #expression_or_statement for #name in #list_or_var
    #expression_or_statement for each #name in #list_or_var

`for _ in range(#int):`

    #int times do
    repeat #int times
    do #int times

`for _ in range(#int):\n\t#expression_or_statement`

    #expression_or_statement #int times do
    repeat #expression_or_statement #int times
    do #expression_or_statement #int times

`for #name in range(0, #int):`

    for #name in 0 to #int
    for #name in 0..#int

`for #name in range(0, #int):\n\t#expression_or_statement`

    #expression_or_statement for #name in 0 to #int
    #expression_or_statement for #name in 0..#int

`while #comparison:`

    while #comparison
    while #comparison do

`while #comparison:\n\t#expression_or_statement`

    #expression_or_statement while #comparison

`while True:`

    while true
    loop

`break`

    break
    exit loop
    end the loop

`continue`

    continue
    next
    jump to the next item in the loop

# statement

- if
- update
- assignment

# expression

- call_function
- operation

# expression_or_statement

- expression
- statement

# value_or_expression

- value
- value
- expression

# comparison

`#value_or_expression == #value_or_expression`

    #value_or_expression == #value_or_expression
    #value_or_expression is #value_or_expression

`#value_or_expression > #value_or_expression`

    #value_or_expression > #value_or_expression
    #value_or_expression gt #value_or_expression
    #value_or_expression is greater than #value_or_expression

# composition

`#condition and #condition`

    #condition and #condition
    #condition && #condition

`#condition or #condition`

    #condition or #condition
    #condition || #condition

# parens_composition

`(#composition)`

    (#composition)

# condition

- comparison
- comparison
- comparison
- nested_condition

# nested_condition

- parens_composition
- composition

# params

`<empty>`

    <empty>
    ()

`#name`

    #name
    (#name)

`#name, #name`

    #name, #name
    #name #name
    (#name, #name)
    (#name #name)

`#name, #name, #name`

    #name, #name, #name
    #name #name, #name
    (#name, #name, #name)
    (#name #name #name)

# args

`<empty>`

    <empty>
    ()

`#value`

    #value
    (#value)

`#value, #value`

    #value, #value
    #value #value
    (#value, #value)
    (#value #value)

`#value, #value, #value`

    #value, #value, #value
    #value #value #value
    (#value, #value, #value)
    (#value #value #value)

# list

`[]`

    []
    ()

`[#value]`

    [#value]
    (#value)

`[#value, #value]`

    [#value, #value]
    (#value, #value)
    (#value #value)
    list of #value and #value

`[#value, #value, #value]`

    [#value, #value, #value]
    (#value, #value, #value)
    (#value #value #value)
    list of #value, #value and #value

# list_or_var

- list
- name
- name

# num_or_var

- number
- name

# string_or_var

- string
- name

# value

- string
- name
- number

# number

- int
- float
