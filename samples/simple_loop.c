#include <stdio.h>

int main() {
    int i = 0;
    while (i < 10) {
        i++;
    }
    // Bug: infinite loop if condition wrong, but here it's fine
    printf("Done\n");
    return 0;
}
