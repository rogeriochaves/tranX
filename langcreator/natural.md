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

- assignment

# value_or_expression

- value
- expression

# condition

- comparison
- composition

# comparison

`$value_or_expression == $value_or_expression`

    $value_or_expression == $value_or_expression
    $value_or_expression is $value_or_expression

`$value_or_expression > $value_or_expression`

    $value_or_expression > $value_or_expression
    $value_or_expression gt $value_or_expression
    $value_or_expression is greater than $value_or_expression

# composition

`$nested_composition and $nested_composition`

    $nested_composition and $nested_composition
    $nested_composition && $nested_composition

`$nested_composition or $nested_composition`

    $nested_composition or $nested_composition
    $nested_composition || $nested_composition

# nested_composition

- parens_composition
- composition
- comparison

# parens_composition

`($composition)`

    ($composition)

# condition

- comparison
- composition

# params

- name
