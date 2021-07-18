# assignment

`#name = #value`

    set #name to #value
    let #name to be #value
    #name = #value

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

`if #condition:\n #expression`

    #expression if #condition

`#assignment if #condition else #value:`

    #assignment if #condition else #value

`if #condition:\n #expression\nelse:\n #expression:`

    #expression if #condition else #expression

# expression

- call_function

# value_or_expression

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

# value

- string
- name
- number

# number

- int
- float
