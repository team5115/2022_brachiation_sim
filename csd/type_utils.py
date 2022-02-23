
def cast_to_int_if_value_is_mathematically_equivalent_to_int(x_i):

    x_label=x_i
    try:
        if (int(x_label)==x_i):
            x_label=int(x_label)
    except Exception as e:
        pass

    return x_label



########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':



   print("________________")


   x1=1.0
   x2=cast_to_int_if_value_is_int(x1)

   print(f"x1={x1}")
   print(f"x2={x2}")


   x1=1.1
   x2=cast_to_int_if_value_is_int(x1)

   print(f"x1={x1}")
   print(f"x2={x2}")

   x1='A'
   x2=cast_to_int_if_value_is_int(x1)

   print(f"x1={x1}")
   print(f"x2={x2}")
