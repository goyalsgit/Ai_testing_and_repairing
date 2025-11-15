#include <stdio.h>

int main() {
    int x;
    scanf("%d", &x);
    if (x > 0) {
        printf("Positive\n");
    } else {
        // Bug: potential division by zero if x == 0, but else covers x <= 0
        printf("Non-positive\n");
    }
    return 0;
}
