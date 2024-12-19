import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const GridVisualization = () => {
  const [step, setStep] = useState(0);
  const gridSize = 7;
  
  const corrupted = [
    [5,4], [4,2], [4,5], [3,0], [2,1], [6,3],
    [2,4], [1,5], [0,6], [3,3], [2,6], [5,1]
  ];
  
  const path = [
    [0,0], [0,1], [1,1], [1,2], [2,2], [3,2],
    [3,1], [4,1], [5,1], [5,2], [5,3], [6,3],
    [6,4], [6,5], [6,6]
  ];

  const renderCell = (x, y) => {
    const isCorrupted = corrupted.some(([cx, cy]) => cx === x && cy === y);
    const pathIndex = path.findIndex(([px, py]) => px === x && py === y);
    const isInCurrentPath = pathIndex !== -1 && pathIndex <= step;
    
    let bgColor = 'bg-gray-100';
    if (isCorrupted) bgColor = 'bg-red-500';
    if (isInCurrentPath) bgColor = 'bg-green-500';
    
    return (
      <div
        key={`${x}-${y}`}
        className={`w-12 h-12 border ${bgColor} flex items-center justify-center`}
      >
        {isCorrupted ? '#' : isInCurrentPath ? 'O' : '.'}
      </div>
    );
  };

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Path-finding Vizualizace</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-7 gap-1">
            {Array.from({ length: gridSize }, (_, y) => (
              <React.Fragment key={y}>
                {Array.from({ length: gridSize }, (_, x) => renderCell(x, y))}
              </React.Fragment>
            ))}
          </div>
          
          <div className="flex gap-2">
            <Button 
              onClick={() => setStep(Math.max(0, step - 1))}
              disabled={step === 0}
              className="w-24"
            >
              Předchozí
            </Button>
            <Button 
              onClick={() => setStep(Math.min(path.length - 1, step + 1))}
              disabled={step === path.length - 1}
              className="w-24"
            >
              Další
            </Button>
          </div>
          
          <div className="text-sm">
            Krok: {step + 1} / {path.length}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default GridVisualization;