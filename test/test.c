#include <stdio.h>


int sum(int n)
{
    if (n == 0)
        return 0;
    return n + sum(n - 2);
}

int main(int argc, char const *argv[])
{
    int i;
    scanf("%d", &i);
    printf("%d", sum(i));
    return 0;
}
