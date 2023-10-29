# Things to do

### General

- ACTUALLY ENFORCE CONSTRAINTS

    Duh...

- Add overlapping open-spaces

    Current implementation splits the open-space into 2 non-overlapping parts

- ~~Add open-space merging~~

    Two adjacent spaces with two alligning corners can easily be merged, to allow for more fits.
    

- Add open-space "pruning" 

    Spaces that can never be filled should be removed. Can only be done with overlapping open-spaces, as in the non-overlapping case spaces might be merged later.

    Spaces that are contained by another space can be removed

- Add shape reservation.

    When adding an item with the anticipation that another item can fill the gap, reserve that item so tha algorithm cant use that item to create and equally size gap again. Rn algorithm adds multiple superitems with the right leftover space that fits a smaller item, but does this more times then there are small items to fill the leftover spaces thus leading to wasted space.


- Ensembles

    Ensemble. Probably different score function


- Allow for shapes composed of different products that have the same dimentions

- Configurations




### Score function

- ~~Wasted space idea~~

    Score function should take into account that while bigger is better, to big might lead to wasted space.

    ![1D score function](/images/ScoreFunction1D.png "1D score function")

    Two regimes cutoff point is the smallest width/height of available items
    - Fill rate:
        Bigger item better

    - Wasted Space:
        Sudden drop as now a lot of space can never be filled. Score increases again when increasing item size as less space is wasted with a maximum for a perfect fit

    Score function extended for 2D, simly multiple two 1D functions (See *Fix dimension dependance in score function*)

    ![2D score function](/images/ScoreFunction2D.png "2D score function")


- ~~Non linear score function~~

    Specifically in the wasted space regime

    Does not seem to help, even harms performance -> removed
    Tried polynomial with different exponents.
    Hypothesis: any superlinear funcion harms performance

    Could change with overlapping open-spaces


- Non linear score function

    In the fill rate regime


- Fix dimension dependance in score function

    Only in non-overlapping open-spaces I think

    Right now score function is calcultated independently for width and height and then multiplied. This is correct when both dimensions are small enough, but could lead to inefficiencies when one or both dimesnions are big enough to introduce wasted space

- Fix min dimension calculation

    Right now this is the min width/height of all of yet available items. Should also take into account that height/witdh might limit item choice.

    Calculation does take into account if items are not availble anymore, but introduce shape reservation here (See *Add shape reservation*)



### Small improvments


- Visualise individual item boundries in shapes

- ~~Fix: shapes that dont fit in layer, should be made.~~

