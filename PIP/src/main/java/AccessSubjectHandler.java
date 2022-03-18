import org.ow2.authzforce.core.pdp.api.AttributeFqn;
import org.ow2.authzforce.core.pdp.api.EvaluationContext;
import org.ow2.authzforce.core.pdp.api.value.*;

import java.util.Iterator;
import java.util.Map;

public class AccessSubjectHandler <AV extends AttributeValue>{
    private String attributeId;
    private DAO dao;
    private Datatype<AV> datatype;
    private EvaluationContext evaluationContext;

    public AccessSubjectHandler(String attributeId, Datatype<AV> datatype, EvaluationContext evaluationContext, DAO dao){
        this.dao = dao;
        this.datatype = datatype;
        this.evaluationContext = evaluationContext;
        this.attributeId = attributeId;
    }

    public AttributeBag<AV> retrieveAttribute(){
        String userId = getID(evaluationContext, "random-id");
        switch(attributeId){
            case "subject-role" :
                if(datatype.equals(StandardDatatypes.STRING)) {
                    if(dao.isOnTheCareStaff(getID(evaluationContext, "ehr-id"), userId))
                        return (AttributeBag<AV>) Bags.singletonAttributeBag(StandardDatatypes.STRING, new StringValue(dao.getRole(userId)));
                    else if(dao.isReceptionist(userId))
                        return (AttributeBag<AV>) Bags.singletonAttributeBag(StandardDatatypes.STRING, new StringValue(dao.getRole(userId)));
                    else
                        return (AttributeBag<AV>) Bags.singletonAttributeBag(StandardDatatypes.STRING, new StringValue(""));
                }
                break;
        }
        return null;
    }

    private String getID(EvaluationContext evaluationContext, String attribute){
        Iterator<Map.Entry<AttributeFqn, AttributeBag<?>>> iterator = evaluationContext.getNamedAttributes();
        String userId = "";

        while(iterator.hasNext()){
            Map.Entry<AttributeFqn, AttributeBag<?>> entry = iterator.next();
            if(entry.getKey().getId().equalsIgnoreCase(attribute)){
                userId = ((StringValue)entry.getValue().elements().iterator().next()).getUnderlyingValue();
            }
        }
        return userId;
    }

}
