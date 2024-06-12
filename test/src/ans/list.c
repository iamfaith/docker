#include "list.h"
#include <stdio.h>
#include <stdlib.h>

bool IsEmpty(Node* head)
{
	return head == NULL ? true : false;
}

void DisplayList(Node *head)
{
	if (IsEmpty(head) == false)
	{
		while (head)
		{
			printf("%f ", head->data);
			head = head->next;
		}
		printf("\n");
	}
}

Node *InsertNode(Node **phead, int index, double x)
{
	Node *currNode = *phead;
	if (currNode == NULL && index > 0)
	{
		return NULL;
	}
	if (currNode == NULL || index == 0)
	{
		Node *temp = (Node *)malloc(sizeof(Node));
		temp->data = x;
		temp->next = NULL;
		if (currNode != NULL)
		{
			temp->next = currNode;
		}
		*phead = temp;
		return temp;
	}
	else
	{
		int currIndex = 0;
		while (currNode && currIndex++ < index - 1)
		{
			currNode = currNode->next;
		}
		if (currNode == NULL && index > 0)
			return NULL;
		Node *temp = (Node *)malloc(sizeof(Node));
		temp->data = x;
		temp->next = currNode->next;
		currNode->next = temp;
		return temp;
	}
}

int FindNode(Node *head, double x)
{
	int pos = 1;
	while (head)
	{
		if (head->data == x)
			return pos;
		pos++;
		head = head->next;
	}
	return 0;
}

int DeleteNode(Node** phead, double x)
{
	Node *currNode = *phead, *preNode = currNode;
	int pos = 1;
	while (currNode)
	{
		if (currNode->data == x)
		{
			// delete head
			if (pos == 1)
			{
				*phead = currNode->next;
			}
			else
			{
				preNode->next = currNode->next;
			}
			free(currNode);
			return pos;
		}
		preNode = currNode;
		pos ++;
		currNode = currNode->next;
	}
	return 0;
}


void DestroyList(Node** phead)
{
	Node *currNode = *phead;
	while (currNode)
	{
		Node* temp = currNode;
		currNode = currNode->next;
		free(temp);
	}	
	*phead = NULL;
}

// Node *InsertNode(Node **phead, int index, double x)
// {
// 	if (index < 0)
// 		return 0;
// 	int currIndex = 1;
// 	Node *currNode = *phead;
// 	while (currNode && index > currIndex)
// 	{
// 		currNode = currNode->next;
// 		currIndex++;
// 	}
// 	if (index > 0 && currNode == 0)
// 		return 0;
// 	Node *newNode = (Node *)malloc(sizeof(Node));
// 	newNode->data = x;
// 	if (index == 0)
// 	{
// 		newNode->next = *phead;
// 		*phead = newNode;
// 	}
// 	else
// 	{
// 		newNode->next = currNode->next;
// 		currNode->next = newNode;
// 	}
// 	return newNode;
// }

int main()
{
	printf("Hello, world\n");
	Node *head = 0;
	for (int i = 0; i < 5; i++)
		InsertNode(&head, i, i);
	DisplayList(head);

	for (int i = 0; i < 5; i++)
		InsertNode(&head, 0, i);
	DisplayList(head);

	InsertNode(&head, 12, 7);
	DisplayList(head);

	for (int i = 0; i < 7; i += 2)
	{
		int idx = FindNode(head, i);
		if (idx > 0)
			printf("%d is at position %d.\n", i, idx);
		else
			printf("%d is not in the list.\n", i);
	}
	DeleteNode(&head, 0);
	DisplayList(head);

	DeleteNode(&head,4);
	DisplayList(head);

	DeleteNode(&head, 7);
	DisplayList(head);

	DestroyList(&head);
	printf("IsEmpty[%d]\n", IsEmpty(head));
}