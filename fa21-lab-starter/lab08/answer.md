## Exercise 1

1. Given the way the address was broken down, how big (in words) are the pages in this model? Leave out the units in your answer (e.g. 4 instead of 4 words).

    8

2. Did you have any Page Hits? (Why?) Can you think of a set of ten addresses that would result in a Page Hit? Your answer should be two [yes/no]'s separated by a comma.

    No. The TLB covers all physical number in physical memory. 

3. What is the process by which we access memory given a virtual address on the very first access assuming a page fault? Order the steps given below. Give your answer as numbers delimited by by a comma with a space, i.e. [num], [num], ... for example, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12.

    1. We update the page table to map the corresponding VPN to the PPN.
    2. Calculate number of virtual page number (VPN) bits through the VA bits and offset bits.
    3. TLB does not contain the VPN so we access the page table for the corresponding VPN.
    4. We access the corresponding word using the offset.
    5. We bring the corresponding virtual page into physical memory from disk.
    6. The page table's entry for VPN has a valid bit of 0.
    7. Get VPN by taking VA[address bits - 1 : offset bits].
    8. Calculate number of offset bits by taking log 2 of page size.
    9. We update the TLB with the corresponding PT entry.
    10. Get offset by taking VA[offset bits - 1 ; 0].
    11. Access TLB for corresponding VPN.
    12. Access given virtual address.

    12, 8, 7, 10, 2, 11, 3, 6, 1, 9, 5, 4

4. How many PPN bits are there?

    2

5. How many VPN bits are there?

    3

6. How many physical pages are there?

    4

7. How many virtual pages are there?

    8

## Exercise 2
00, 20, 40, 60, 80, A0, C0, E0, 00, 20

## Exercise 3
Increase Physical Memory Size, decrease Page Size

## Exercise 4
P1, P2, P3, P4 are four different processes. When it comes to another process, it will clear the TLB, and causes higher TLB Miss Rate.