#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

char *rand_string(size_t length)
{
    char *str = NULL;

    const char charset[] =
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=!@#$%^&*_+;',./:<>?`~";

    str = malloc(length + 1);

    for (size_t i = 0; i < length; i++)
    {
        int key = rand() % (int) (sizeof charset - 1);
        str[i] = charset[key];
    }

    str[length] = '\0';

    return str;
}

int main()
{
    printf("Password length: ");

    int length;
    scanf("%d", &length);

    srand(time(NULL));

    char *randstr = rand_string(length);

    printf("%s\nLength: %lu\n", randstr, strlen(randstr));
}
