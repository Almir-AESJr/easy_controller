export class Matriz {

  label: string | undefined;
  lines: number = 1;
  cols: number = 1;
  values: number[][] =  Array.from(Array(this.lines), () => new Array(this.cols));


  constructor(label: string | undefined) {
    this.label = label;
  }
}
