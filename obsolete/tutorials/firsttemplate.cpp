#include <string>
#include <iostream>

template <typename T> 
void switching(T &x, T &y)
{
    T temp = x;
    x = y;
    y = temp;
}


template <typename T>
void printing(T x, T y)
{
    std::cout << "This is a: " << x << std::endl;
    std::cout << "This is b: " << y << std::endl;
}


int main()
{
    int a = 10;
    int b = 20;

    std::string pirmas = "abc";
    std::string antras = "def";

    printing<int>(a,b);

    switching<int>(a,b);

    printing<int>(a,b);

    
    printing<std::string>(pirmas, antras);

    switching<std::string>(pirmas, antras);

    printing<std::string>(pirmas, antras);

    return 0;
}
