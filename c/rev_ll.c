#include <stdio.h>
#include <stdlib.h>

struct node {
  int data;
  struct node *next;
};

struct ll {
  struct node *head;
};

void ll_print(struct ll *ll) {
  for (struct node *curr = ll->head; curr; curr = curr->next) {
    printf("%d ", curr->data);
  }

  printf("\n");
}

void ll_finish(struct ll *ll) {
  for (struct node *tmp = NULL; ll->head;) {
    tmp = ll->head;

    ll->head = tmp->next;

    free(tmp);
  }
}

void ll_reverse(struct ll *ll) {
  struct node *prev = NULL, *curr = ll->head, *next = NULL;

  while (curr) {
    next = curr->next;
    curr->next = prev;
    prev = curr;
    curr = next;
  }

  ll->head = prev;
}

struct node *node_add(struct node *node, int data) {
  node->next = calloc(1, sizeof(*node->next));

  if (node->next) {
    node->next->data = data;
  }

  return node->next;
}

int main() {
  struct ll ll = {.head = calloc(1, sizeof(*ll.head))};

  if (!ll.head) {
    return EXIT_FAILURE;
  }

  struct node *curr = ll.head;

  for (size_t i = 1; i < 10; i++) {
    curr = node_add(curr, i);

    if (!curr) {
      ll_finish(&ll);

      return EXIT_FAILURE;
    }
  }

  ll_print(&ll);
  ll_reverse(&ll);
  ll_print(&ll);
  ll_finish(&ll);
}
